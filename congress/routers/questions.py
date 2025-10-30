# Fichier : congress/routers/questions.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import aliased, Session
from sqlalchemy import select
from typing import List

from .. import models, schemas
from ..dependencies import get_db


router = APIRouter(
    prefix="/questions",
    tags=["questions"]
)

Participant = aliased(models.Participant)
SessionModel = aliased(models.Session)
Question = models.Question
Orateur = models.Orateur


# --- Helpers
def question_to_schema(q: models.Question, db: Session) -> schemas.QuestionResponse:
    session = db.query(models.Session).filter(models.Session.id == q.session_id).first()
    participant = None
    if q.participant_id:
        p = db.query(models.Participant).filter(models.Participant.id == q.participant_id).first()
        if p:
            participant = f"{p.prenom} {p.nom}"

    return schemas.QuestionResponse(
        id=q.id,
        question_text=q.question_text,
        created_at=q.created_at,
        status=q.status,
        session=session.titre if session else "Inconnue",
        participant=participant,
        orateur=(q.orateur.nom if getattr(q, "orateur", None) else None),
    )


# --- Routes ---

@router.post("", response_model=schemas.QuestionResponse)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    session = db.query(models.Session).filter(models.Session.id == question.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session introuvable")

    if session.orateurs:
        if question.orateur_id is None:
            raise HTTPException(422, "orateur_id est requis pour cette session")
        if not any(o.id == question.orateur_id for o in session.orateurs):
            raise HTTPException(400, "Cet orateur n'est pas associé à la session")

    if question.participant_id:
        participant = db.query(models.Participant).filter(models.Participant.id == question.participant_id).first()
        if not participant:
            raise HTTPException(status_code=404, detail="Participant introuvable")

    q = models.Question(
        question_text=question.question_text,
        status="non_repondu",
        session_id=question.session_id,
        participant_id=question.participant_id,
        orateur_id=question.orateur_id
    )

    db.add(q)
    db.commit()
    db.refresh(q)
    return schemas.QuestionResponse(
        id=q.id,
        question_text=q.question_text,
        created_at=q.created_at,
        status=q.status,
        session=session.titre,
        participant=(q.participant.nom if getattr(q, "participant", None) else None),
        orateur=(q.orateur.nom if getattr(q, "orateur", None) else None),
    )



@router.get("", response_model=list[schemas.QuestionResponse])
def list_questions(
        session_id: int,
        status: str | None = None,
        orateur_id: int | None = None,
        db: Session = Depends(get_db),
):

    if status not in (None, "non_repondu", "repondu"):
        raise HTTPException(status_code=400, detail="Statut invalide")

    stmt = (
        select(
            Question,
            SessionModel.titre,
            Participant.prenom,
            Participant.nom,
            Orateur.nom,
        )
        .join(SessionModel, SessionModel.id == Question.session_id)
        .outerjoin(Participant, Participant.id == Question.participant_id)
        .outerjoin(Orateur, Orateur.id == Question.orateur_id)
        .where(Question.session_id == session_id)
    )

    if status:
        stmt = stmt.where(Question.status == status)

    if orateur_id:
        stmt = stmt.where(Question.orateur_id == orateur_id)

    stmt = stmt.order_by(Orateur.nom.asc(), Question.created_at.asc())

    rows = db.execute(stmt).all()

    out: list[schemas.QuestionResponse] = []
    for q, session_titre, p_prenom, p_nom, orateur_nom in rows:
        participant = (
            f"{(p_prenom or '').strip()} {(p_nom or '').strip()}".strip()
            if (p_prenom or p_nom) else None
        )
        out.append(
            schemas.QuestionResponse(
                id=q.id,
                question_text=q.question_text,
                created_at=q.created_at,
                status=q.status,
                session=session_titre,
                participant=participant,
                orateur=orateur_nom,
            )
        )
    return out


@router.patch("/{question_id}/toggle", response_model=schemas.QuestionResponse)
def toggle_status(question_id: int, db: Session = Depends(get_db)):
    q = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question non trouvée")

    q.status = "repondu" if q.status == "non_repondu" else "non_repondu"
    db.commit()
    db.refresh(q)
    return question_to_schema(q, db)