from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from .database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    status = Column(String(20), default="non_repondu")

class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    profession = Column(String(255))
    role = Column(String(20), default="participant")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String(255), nullable=False)
    heure_debut = Column(TIMESTAMP, nullable=False)
    heure_fin = Column(TIMESTAMP, nullable=False)
    conferencier = Column(String(255))
    salle = Column(String(100))