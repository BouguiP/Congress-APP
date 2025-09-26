from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from congress import models, schemas
from congress.database import engine
from congress.dependencies import get_db
from sqlalchemy import and_, Date, or_
from datetime import datetime




models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Congress App")

@app.get("/questions", response_model=list[schemas.QuestionResponse])
def read_questions(
        status: str | None = None,
        session_id: int | None = None,
        db: Session = Depends(get_db)
):
    query = db.query(models.Question)

    if status:
        if status not in ["non_repondu", "repondu"]:
            raise HTTPException(status_code=400, detail="Statut invalide")
        query = query.filter(models.Question.status == status)

    if session_id:
        query = query.filter(models.Question.session_id == session_id)

    return query.all()



@app.post("/questions", response_model=schemas.QuestionResponse)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    # Vérifie que la session_id est fournie
    if not question.session_id:
        raise HTTPException(status_code=400, detail="Une session doit être sélectionnée")

    # Vérifie que la session existe
    session = db.query(models.Session).filter(models.Session.id == question.session_id).first()
    if not session:
        raise HTTPException(status_code=400, detail="Session inexistante")

    new_question = models.Question(
        session_id=question.session_id,
        question_text=question.question_text,
        status="non_repondu"
    )
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question


# Inverser le statut (PATCH)
@app.patch("/questions/{question_id}/toggle", response_model=schemas.QuestionResponse)
def toggle_status(question_id: int, db: Session = Depends(get_db)):
    question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question non trouvée")

    question.status = "repondu" if question.status == "non_repondu" else "non_repondu"
    db.commit()
    db.refresh(question)
    return question


@app.post("/participants", response_model=schemas.ParticipantResponse)
def create_participant(participant: schemas.ParticipantCreate, db: Session = Depends(get_db)):
    # Vérifie si email déjà pris
    existing = db.query(models.Participant).filter(models.Participant.email == participant.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    new_participant = models.Participant(
        nom=participant.nom,
        prenom=participant.prenom,
        email=participant.email,
        profession=participant.profession
    )

    db.add(new_participant)
    db.commit()
    db.refresh(new_participant)
    return new_participant

@app.get("/participants/{participant_id}", response_model=schemas.ParticipantResponse)
def get_participant(participant_id: int, db: Session = Depends(get_db)):
    participant = db.query(models.Participant).filter(models.Participant.id == participant_id).first()
    if not participant:
        raise HTTPException(status_code=404, detail="Participant non trouvé")
    return participant

# Créer une session
@app.post("/sessions", response_model=schemas.SessionResponse)
def create_session(session: schemas.SessionCreate, db: Session = Depends(get_db)):
    # Vérif 1 : heure_fin > heure_debut
    if session.heure_fin <= session.heure_debut:
        raise HTTPException(status_code=400, detail="L'heure de fin doit être après l'heure de début")

    # Vérif 2 : chevauchement salle
    if session.salle:
        conflict_salle = db.query(models.Session).filter(
            models.Session.salle == session.salle,
            or_(
                and_(session.heure_debut >= models.Session.heure_debut, session.heure_debut < models.Session.heure_fin),
                and_(session.heure_fin > models.Session.heure_debut, session.heure_fin <= models.Session.heure_fin),
                and_(session.heure_debut <= models.Session.heure_debut, session.heure_fin >= models.Session.heure_fin)
            )
        ).first()
        if conflict_salle:
            raise HTTPException(status_code=400, detail=f"Salle {session.salle} déjà occupée sur ce créneau")

    # Vérif 3 : chevauchement conférencier
    if session.conferencier:
        conflict_conf = db.query(models.Session).filter(
            models.Session.conferencier == session.conferencier,
            or_(
                and_(session.heure_debut >= models.Session.heure_debut, session.heure_debut < models.Session.heure_fin),
                and_(session.heure_fin > models.Session.heure_debut, session.heure_fin <= models.Session.heure_fin),
                and_(session.heure_debut <= models.Session.heure_debut, session.heure_fin >= models.Session.heure_fin)
            )
        ).first()
        if conflict_conf:
            raise HTTPException(status_code=400, detail=f"Conférencier {session.conferencier} déjà occupé sur ce créneau")

    # Si tout est OK, on crée la session
    new_session = models.Session(
        titre=session.titre,
        heure_debut=session.heure_debut,
        heure_fin=session.heure_fin,
        conferencier=session.conferencier,
        salle=session.salle
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session


# Récupérer toutes les sessions d’une date
@app.get("/sessions", response_model=list[schemas.SessionResponse])
def get_sessions(date: datetime | None = None, db: Session = Depends(get_db)):
    query = db.query(models.Session)
    if date:
        # on filtre par jour
        query = query.filter(models.Session.heure_debut.cast(Date) == date.date())
    return query.order_by(models.Session.heure_debut).all()


# Session en cours
@app.get("/sessions/current", response_model=schemas.SessionResponse | None)
def get_current_session(db: Session = Depends(get_db)):
    now = datetime.now()
    session = db.query(models.Session).filter(
        and_(
            models.Session.heure_debut <= now,
            models.Session.heure_fin >= now
        )
    ).first()
    return session


# Prochaine session
@app.get("/sessions/next", response_model=schemas.SessionResponse | None)
def get_next_session(db: Session = Depends(get_db)):
    now = datetime.now()
    session = db.query(models.Session).filter(
        models.Session.heure_debut > now
    ).order_by(models.Session.heure_debut).first()
    return session