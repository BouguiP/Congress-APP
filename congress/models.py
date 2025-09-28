from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Text, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy.sql import func



class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(50), unique=True, nullable=False)  # corrigé : nom

    participants = relationship("Participant", back_populates="role")


class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    profession = Column(String(255), nullable=False)
    password = Column(String(255), nullable=True)

    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", back_populates="participants")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String(255), nullable=False)
    heure_debut = Column(TIMESTAMP, nullable=False)
    heure_fin = Column(TIMESTAMP, nullable=False)
    conferenciers = Column(Text, nullable=False)  # CSV
    salle = Column(String(100), nullable=False)


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    status = Column(String(20), default="non_repondu")

    session_id = Column(Integer, ForeignKey("sessions.id"))
    participant_id = Column(Integer, ForeignKey("participants.id"), nullable=True)
