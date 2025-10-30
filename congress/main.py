import os

from fastapi import FastAPI, Request

from congress import models, schemas
from congress.database import engine

from fastapi.staticfiles import StaticFiles

from fastapi.middleware.cors import CORSMiddleware

from urllib.parse import quote


from .routers import questions
from .routers import questions, sessions, participants


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Congress App")

STATIC_DIR = "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helpers


def _human_size(n: int) -> str:
    # n en octets -> libellé
    for unit in ["B", "KB", "MB", "GB"]:
        if n < 1024.0 or unit == "GB":
            return f"{n:.0f} {unit}" if unit != "MB" else f"{n/1024:.1f} MB"
        n /= 1024.0
    return f"{n:.0f} B"



# -------------------------
# DOCUMENTS (menu, attestation, etc.)
# -------------------------

# Récupérer un document par clé (ex: "menu", "attestation")
@app.get("/documents", response_model=list[schemas.DocItem])
def get_documents(request: Request):
    base = str(request.base_url).rstrip("/")  # ex: https://xxxxx.ngrok-free.dev
    docs = []
    for file in os.listdir(STATIC_DIR):
        path = os.path.join(STATIC_DIR, file)
        if not os.path.isfile(path):
            continue
        ext = file.split(".")[-1].lower() if "." in file else "unknown"
        size_label = f"{_human_size(os.path.getsize(path))} • {ext.upper()}"
        # protéger espaces/caractères spéciaux
        url = f"{base}/static/{quote(file)}"
        docs.append({"name": file, "url": url, "type": ext, "size_label": size_label})
    return docs

app.include_router(questions.router)
app.include_router(sessions.router)
app.include_router(participants.router)