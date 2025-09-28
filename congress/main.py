from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from congress import models, schemas
from congress.database import engine
from congress.dependencies import get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Congress App")


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
        role=p.role.nom,  # corrigé
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
        participant=participant
    )


# Rôles
@app.get("/roles", response_model=list[schemas.RoleResponse])
def list_roles(db: Session = Depends(get_db)):
    roles = db.query(models.Role).all()
    return [schemas.RoleResponse(id=r.id, nom=r.nom) for r in roles]  # corrigé


# Participants

@app.post("/participants/register", response_model=schemas.ParticipantResponse)
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
@app.post("/sessions", response_model=schemas.SessionResponse)
def create_session(session: schemas.SessionCreate, db: Session = Depends(get_db)):
    s = models.Session(
        titre=session.titre,
        heure_debut=session.heure_debut,
        heure_fin=session.heure_fin,
        conferenciers=",".join(session.conferenciers),
        salle=session.salle
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    return session_to_schema(s)


@app.get("/sessions", response_model=list[schemas.SessionResponse])
def list_sessions(db: Session = Depends(get_db)):
    sessions = db.query(models.Session).all()
    return [session_to_schema(s) for s in sessions]


# Questions
@app.post("/questions", response_model=schemas.QuestionResponse)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    session = db.query(models.Session).filter(models.Session.id == question.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session introuvable")

    if question.participant_id:
        participant = db.query(models.Participant).filter(models.Participant.id == question.participant_id).first()
        if not participant:
            raise HTTPException(status_code=404, detail="Participant introuvable")

    q = models.Question(
        question_text=question.question_text,
        status="non_repondu",
        session_id=question.session_id,
        participant_id=question.participant_id
    )
    db.add(q)
    db.commit()
    db.refresh(q)
    return question_to_schema(q, db)


@app.get("/questions", response_model=list[schemas.QuestionResponse])
def list_questions(session_id: int, status: str | None = None, db: Session = Depends(get_db)):
    query = db.query(models.Question).filter(models.Question.session_id == session_id)

    if status:
        if status not in ["non_repondu", "repondu"]:
            raise HTTPException(status_code=400, detail="Statut invalide")
        query = query.filter(models.Question.status == status)

    questions = query.all()
    return [question_to_schema(q, db) for q in questions]


@app.patch("/questions/{question_id}/toggle", response_model=schemas.QuestionResponse)
def toggle_status(question_id: int, db: Session = Depends(get_db)):
    q = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question non trouvée")

    q.status = "repondu" if q.status == "non_repondu" else "non_repondu"
    db.commit()
    db.refresh(q)
    return question_to_schema(q, db)
