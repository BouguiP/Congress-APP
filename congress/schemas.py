from pydantic import BaseModel, EmailStr
from datetime import datetime

class QuestionCreate(BaseModel):
    session_id: int
    question_text: str


class QuestionResponse(BaseModel):
    id: int
    question_text: str
    created_at: datetime
    status: str

    model_config = {
        "from_attributes": True
    }

class QuestionStatusUpdate(BaseModel):
    status: str

class ParticipantCreate(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    profession: str | None = None

class ParticipantResponse(BaseModel):
    id: int
    nom: str
    prenom: str
    email: EmailStr
    profession: str | None
    role: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class SessionCreate(BaseModel):
    titre: str
    heure_debut: datetime
    heure_fin: datetime
    conferencier: str | None = None
    salle: str | None = None

class SessionResponse(BaseModel):
    id: int
    titre: str
    heure_debut: datetime
    heure_fin: datetime
    conferencier: str | None
    salle: str | None

    model_config = {
        "from_attributes": True
    }