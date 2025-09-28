from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class RoleResponse(BaseModel):
    id: int
    nom: str   # corrigé

    class Config:
        from_attributes = True


class ParticipantCreate(BaseModel):
    nom: str
    prenom: str
    email: str
    profession: str
    role_id: int
    password: Optional[str] = None


class ParticipantResponse(BaseModel):
    id: int
    nom: str
    prenom: str
    email: str
    profession: str
    role: str   # nom du rôle
    created_at: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    message: str
    role: str


class SessionCreate(BaseModel):
    titre: str
    heure_debut: datetime
    heure_fin: datetime
    conferenciers: List[str]
    salle: str


class SessionResponse(BaseModel):
    id: int
    titre: str
    heure_debut: datetime
    heure_fin: datetime
    conferenciers: List[str]
    salle: str

    class Config:
        from_attributes = True


class QuestionCreate(BaseModel):
    question_text: str
    session_id: int
    participant_id: Optional[int] = None


class QuestionResponse(BaseModel):
    id: int
    question_text: str
    created_at: datetime
    status: str
    session: str
    participant: Optional[str] = None

    class Config:
        from_attributes = True
