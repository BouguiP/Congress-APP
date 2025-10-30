import os

from fastapi import FastAPI, Depends, HTTPException, Request
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
from datetime import timezone
import pytz
from urllib.parse import quote
from .routers import questions


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Congress App")

TZ_PARIS = pytz.timezone("Europe/Paris")
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
def hhmm(dt):
    if dt is None:
        return None
    return dt.astimezone(TZ_PARIS).strftime("%H:%M")


def session_to_schema(s: models.Session) -> schemas.SessionResponse:
    return schemas.SessionResponse(
        id=s.id,
        titre=s.titre,
        heure_debut=s.heure_debut,
        heure_fin=s.heure_fin,
        conferenciers=[c for c in s.conferenciers.split(",") if c.strip()],
        salle=s.salle,
        heure_debut_hhmm=hhmm(s.heure_debut),
        heure_fin_hhmm=hhmm(s.heure_fin)
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



def _human_size(n: int) -> str:
    # n en octets -> libellé
    for unit in ["B", "KB", "MB", "GB"]:
        if n < 1024.0 or unit == "GB":
            return f"{n:.0f} {unit}" if unit != "MB" else f"{n/1024:.1f} MB"
        n /= 1024.0
    return f"{n:.0f} B"

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
    now = datetime.now(paris).replace(tzinfo=None)
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



# -------------------------
# DOCUMENTS (menu, attestation, etc.)
# -------------------------

# Récupérer un document par clé (ex: "menu", "attestation")
@app.get("/documents", response_model=list[schemas.DocItem])
def get_documents(request: Request):
    base = str(request.base_url).rstrip("/")  # ex: https://xxxxx.ngrok-free.dev
    docs = []
    for file in os.listdir(STATIC_DIR):
        path = os.path.join(STATIC_DIR, file)
        if not os.path.isfile(path):
            continue
        ext = file.split(".")[-1].lower() if "." in file else "unknown"
        size_label = f"{_human_size(os.path.getsize(path))} • {ext.upper()}"
        # protéger espaces/caractères spéciaux
        url = f"{base}/static/{quote(file)}"
        docs.append({"name": file, "url": url, "type": ext, "size_label": size_label})
    return docs

app.include_router(questions.router)