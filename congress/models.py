from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from .database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    status = Column(String(20), default="non_repondu")
