from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List



class OrateurOut(BaseModel):
    id: int
    nom: str
    class Config:
        from_attributes = True


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
    role: Optional[str]   # nom du rôle
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
    orateur_ids: List[int]
    salle: str


class SessionResponse(BaseModel):
    id: int
    titre: str
    heure_debut: datetime
    heure_fin: datetime
    conferenciers: List[str]
    salle: str
    heure_debut_hhmm: Optional[str] = None
    heure_fin_hhmm: Optional[str] = None

    class Config:
        from_attributes = True


class QuestionCreate(BaseModel):
    question_text: str
    session_id: int
    participant_id: Optional[int] = None
    orateur_id: Optional[int] = None


class QuestionResponse(BaseModel):
    id: int
    question_text: str
    created_at: datetime
    status: str
    session: str
    participant: Optional[str] = None
    orateur: Optional[str] = None

    class Config:
        from_attributes = True

class DocumentUpsert(BaseModel):
    content: Optional[str] = None
    file_url: Optional[str] = None

class DocumentResponse(BaseModel):
    key: str
    content: Optional[str] = None
    file_url: Optional[str] = None
    updated_at: datetime
    model_config = {"from_attributes": True}

class DocItem(BaseModel):
    name: str
    url: str
    type: str
    size_label: Optional[str] = None