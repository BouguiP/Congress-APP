import os

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from congress import models, schemas
from congress.database import engine
from congress.dependencies import get_db
from datetime import datetime
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from sqlalchemy.orm import aliased
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from congress.models import Question, Orateur
from zoneinfo import ZoneInfo



models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Congress App")

STATIC_DIR = "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

Participant = aliased(models.Participant)
SessionModel = aliased(models.Session)
Question = models.Question


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helpers
def session_to_schema(s: models.Session) -> schemas.SessionResponse:
    return schemas.SessionResponse(
        id=s.id,
        titre=s.titre,
        heure_debut=s.heure_debut,
        heure_fin=s.heure_fin,
        conferenciers=[c for c in s.conferenciers.split(",") if c.strip()],
        salle=s.salle
    )


def participant_to_schema(p: models.Participant) -> schemas.ParticipantResponse:
    return schemas.ParticipantResponse(
        id=p.id,
        nom=p.nom,
        prenom=p.prenom,
        email=p.email,
        profession=p.profession,
        role=(p.role.nom if p.role else None),
        created_at=p.created_at
    )


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


# Rôles
@app.get("/roles", response_model=list[schemas.RoleResponse])
def list_roles(db: Session = Depends(get_db)):
    roles = db.query(models.Role).all()
    return [schemas.RoleResponse(id=r.id, nom=r.nom) for r in roles]


# Participants
@app.post("/participants/register", response_model=schemas.ParticipantResponse)
def register_participant(payload: schemas.ParticipantCreate, db: Session = Depends(get_db)):
    # Vérifier email unique
    existing = db.query(models.Participant).filter(models.Participant.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    # Vérifier rôle
    role = db.query(models.Role).filter(models.Role.id == payload.role_id).first()
    if not role:
        raise HTTPException(status_code=400, detail="Rôle invalide")

    # Si rôle moderateur/admin -> mot de passe requis (stockage en clair)
    if role.nom in ("moderateur", "admin"):
        if not payload.password:
            raise HTTPException(status_code=400, detail="Mot de passe requis pour ce rôle")
        stored_password = payload.password
    else:
        stored_password = None

    p = models.Participant(
        nom=payload.nom,
        prenom=payload.prenom,
        email=payload.email,
        profession=payload.profession,
        role_id=payload.role_id,
        password=stored_password
    )

    db.add(p)
    db.commit()
    db.refresh(p)

    return schemas.ParticipantResponse(
        id=p.id,
        nom=p.nom,
        prenom=p.prenom,
        email=p.email,
        profession=p.profession,
        role=p.role.nom if p.role else None,
        created_at=p.created_at
    )



@app.post("/login", response_model=schemas.LoginResponse)
def login(login_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.Participant).filter(models.Participant.email == login_data.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Identifiants invalides")

    if not user.password or user.password != login_data.password:
        raise HTTPException(status_code=401, detail="Identifiants invalides")

    return {"message": "Connexion réussie", "role": user.role.nom if user.role else "unknown"}
# Sessions
@app.post("/sessions", response_model=schemas.SessionResponse, status_code=201)
def create_session(payload: schemas.SessionCreate, db: Session = Depends(get_db)):
    # 1) début < fin
    if payload.heure_fin <= payload.heure_debut:
        raise HTTPException(status_code=400, detail="heure_fin doit être strictement > heure_debut")

    overlapping = db.query(models.Session).filter(
        models.Session.heure_debut < payload.heure_fin,
        models.Session.heure_fin > payload.heure_debut
    ).all()

    obj = models.Session(
        titre=payload.titre,
        heure_debut=payload.heure_debut,
        heure_fin=payload.heure_fin,
        conferenciers=",".join([s.strip() for s in (payload.conferenciers or [])]),
        salle=payload.salle,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return session_to_schema(obj)


@app.get("/sessions", response_model=list[schemas.SessionResponse])
def list_sessions(db: Session = Depends(get_db)):
    sessions = db.query(models.Session).all()
    return [session_to_schema(s) for s in sessions]

# --- SESSIONS EN COURS ---
@app.get("/sessions/current", response_model=list[schemas.SessionResponse])
def get_current_sessions(db: Session = Depends(get_db)):
    paris = ZoneInfo("Europe/Paris")
    now = datetime.now(paris).replace(tzinfo=None)    # pour MVP on reste en naive; plus tard: ZoneInfo("Europe/Paris")
    rows = (
        db.query(models.Session)
        .filter(models.Session.heure_debut <= now, models.Session.heure_fin > now)
        .all()
    )
    return [session_to_schema(s) for s in rows]

# --- PROCHAINE SESSION ---
@app.get("/sessions/next", response_model=schemas.SessionResponse)
def get_next_session(db: Session = Depends(get_db)):
    paris = ZoneInfo("Europe/Paris")
    now = datetime.now(paris).replace(tzinfo=None)

    s = (
        db.query(models.Session)
        .filter(models.Session.heure_debut > now)
        .order_by(models.Session.heure_debut.asc())
        .first()
    )
    if not s:
        raise HTTPException(status_code=404, detail="Aucune session à venir")
    return session_to_schema(s)

@app.get("/sessions/{session_id}/orateurs", response_model=List[schemas.OrateurOut])
def list_orateurs_for_session(session_id: int, db: Session = Depends(get_db)):
    s = db.query(models.Session).get(session_id)
    if not s:
        raise HTTPException(status_code=404, detail="Session not found")
    return [schemas.OrateurOut.from_orm(o) for o in s.orateurs]

# Questions
@app.post("/questions", response_model=schemas.QuestionResponse)
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


@app.get("/questions", response_model=list[schemas.QuestionResponse])
def list_questions(
        session_id: int,
        status: str | None = None,
        orateur_id: int | None = None,   # <-- nouveau filtre
        db: Session = Depends(get_db),
):
    # filtre de statut si fourni
    if status not in (None, "non_repondu", "repondu"):
        raise HTTPException(status_code=400, detail="Statut invalide")

    stmt = (
        select(
            Question,                  # l'objet question
            SessionModel.titre,        # titre de la session
            Participant.prenom,        # prénom participant (peut être None)
            Participant.nom,           # nom participant (peut être None)
            Orateur.nom,               # <-- nom orateur (peut être None)
        )
        .join(SessionModel, SessionModel.id == Question.session_id)
        .outerjoin(Participant, Participant.id == Question.participant_id)
        .outerjoin(Orateur, Orateur.id == Question.orateur_id)   # <-- jointure orateur
        .where(Question.session_id == session_id)
    )

    if status:
        stmt = stmt.where(Question.status == status)

    if orateur_id:
        stmt = stmt.where(Question.orateur_id == orateur_id)     # <-- filtre orateur

    # tri : par nom d'orateur puis par date de création
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
                orateur=orateur_nom,   # <-- renvoyé dans la réponse
            )
        )
    return out


@app.patch("/questions/{question_id}/toggle", response_model=schemas.QuestionResponse)
def toggle_status(question_id: int, db: Session = Depends(get_db)):
    q = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question non trouvée")

    q.status = "repondu" if q.status == "non_repondu" else "non_repondu"
    db.commit()
    db.refresh(q)
    return question_to_schema(q, db)


# -------------------------
# DOCUMENTS (menu, attestation, etc.)
# -------------------------

# Récupérer un document par clé (ex: "menu", "attestation")
@app.get("/documents")
def get_documents():
    files = os.listdir(STATIC_DIR)  # liste tous les fichiers du dossier
    documents = []

    for file in files:
        ext = file.split(".")[-1].lower() if "." in file else "unknown"
        documents.append({
            "name": file,
            "url": f"/static/{file}",
            "type": ext
        })

    return documents
