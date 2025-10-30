
from fastapi import FastAPI
from congress import models
from congress.database import engine
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .routers import questions, sessions, participants, documents


models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Congress App")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(questions.router)
app.include_router(sessions.router)
app.include_router(participants.router)
app.include_router(documents.router)