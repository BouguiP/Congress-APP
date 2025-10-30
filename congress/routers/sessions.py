# Fichier : congress/routers/sessions.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from zoneinfo import ZoneInfo
import pytz

from .. import models, schemas
from ..dependencies import get_db

router = APIRouter(
    prefix="/sessions",
    tags=["sessions"]
)

TZ_PARIS = pytz.timezone("Europe/Paris")

def hhmm(dt):
    if dt is None:
        return None
    return dt.astimezone(TZ_PARIS).strftime("%H:%M")


# --- Helpers

def session_to_schema(s: models.Session) -> schemas.SessionResponse:
    return schemas.SessionResponse(
        id=s.id,
        titre=s.titre,
        heure_debut=s.heure_debut,
        heure_fin=s.heure_fin,
        conferenciers=[orateur.nom for orateur in s.orateurs],
        salle=s.salle,
        heure_debut_hhmm=hhmm(s.heure_debut),
        heure_fin_hhmm=hhmm(s.heure_fin)
    )


# --- Routes ---

@router.post("", response_model=schemas.SessionResponse, status_code=201)
def create_session(payload: schemas.SessionCreate, db: Session = Depends(get_db)):

    if payload.heure_fin <= payload.heure_debut:
        raise HTTPException(status_code=400, detail="heure_fin doit être strictement > heure_debut")

    overlapping = db.query(models.Session).filter(
        models.Session.heure_debut < payload.heure_fin,
        models.Session.heure_fin > payload.heure_debut
    ).all()

    orateurs = []
    if payload.orateur_ids:

        orateurs = db.query(models.Orateur).filter(models.Orateur.id.in_(payload.orateur_ids)).all()

        if len(orateurs) != len(set(payload.orateur_ids)):
            raise HTTPException(status_code=400, detail="Un ou plusieurs ID d'orateurs sont invalides")


    obj = models.Session(
        titre=payload.titre,
        heure_debut=payload.heure_debut,
        heure_fin=payload.heure_fin,
        salle=payload.salle,
        orateurs=orateurs,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return session_to_schema(obj)


@router.get("", response_model=list[schemas.SessionResponse])
def list_sessions(db: Session = Depends(get_db)):
    sessions = db.query(models.Session).all()
    return [session_to_schema(s) for s in sessions]


@router.get("/current", response_model=list[schemas.SessionResponse])
def get_current_sessions(db: Session = Depends(get_db)):
    paris = ZoneInfo("Europe/Paris")
    now = datetime.now(paris).replace(tzinfo=None)
    rows = (
        db.query(models.Session)
        .filter(models.Session.heure_debut <= now, models.Session.heure_fin > now)
        .all()
    )
    return [session_to_schema(s) for s in rows]


@router.get("/next", response_model=schemas.SessionResponse)
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


@router.get("/{session_id}/orateurs", response_model=List[schemas.OrateurOut])
def list_orateurs_for_session(session_id: int, db: Session = Depends(get_db)):
    s = db.query(models.Session).get(session_id)
    if not s:
        raise HTTPException(status_code=404, detail="Session not found")
    return [schemas.OrateurOut.from_orm(o) for o in s.orateurs]