from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..dependencies import get_db

router = APIRouter(
    tags=["participants & authentification"]
)

# --- Helper
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

# --- Routes

@router.get("/roles", response_model=list[schemas.RoleResponse])
def list_roles(db: Session = Depends(get_db)):
    roles = db.query(models.Role).all()
    return [schemas.RoleResponse(id=r.id, nom=r.nom) for r in roles]


@router.post("/participants/register", response_model=schemas.ParticipantResponse)
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


@router.post("/login", response_model=schemas.LoginResponse)
def login(login_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.Participant).filter(models.Participant.email == login_data.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Identifiants invalides")

    if not user.password or user.password != login_data.password:
        raise HTTPException(status_code=401, detail="Identifiants invalides")

    return {"message": "Connexion réussie", "role": user.role.nom if user.role else "unknown"}