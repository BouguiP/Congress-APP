from pydantic import BaseModel
from datetime import datetime

class QuestionCreate(BaseModel):
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