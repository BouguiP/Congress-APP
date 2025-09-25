from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from congress import models, schemas
from congress.database import engine
from congress.dependencies import get_db



models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Congress App")


@app.get("/questions", response_model=list[schemas.QuestionResponse])
def read_questions(status: str | None = None, db: Session = Depends(get_db)):
    query = db.query(models.Question)

    if status:
        if status not in ["non_repondu", "repondu"]:
            raise HTTPException(status_code=400, detail="Statut invalide")
        query = query.filter(models.Question.status == status)

    return query.all()


@app.post("/questions", response_model=schemas.QuestionResponse)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    new_question = models.Question(
        question_text=question.question_text,
        status="non_repondu"
    )
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question

# Inverser le statut (PATCH)
@app.patch("/questions/{question_id}/toggle", response_model=schemas.QuestionResponse)
def toggle_status(question_id: int, db: Session = Depends(get_db)):
    question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question non trouvée")

    question.status = "repondu" if question.status == "non_repondu" else "non_repondu"
    db.commit()
    db.refresh(question)
    return question


