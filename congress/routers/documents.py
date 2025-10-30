# Fichier : congress/routers/documents.py

import os
from fastapi import APIRouter, Request
from urllib.parse import quote
from typing import List

from .. import schemas

router = APIRouter(
    prefix="/documents",
    tags=["documents"]
)

STATIC_DIR = "static"

# --- Helper
def _human_size(n: int) -> str:
    # n en octets -> libellé
    for unit in ["B", "KB", "MB", "GB"]:
        if n < 1024.0 or unit == "GB":
            return f"{n:.0f} {unit}" if unit != "MB" else f"{n/1024:.1f} MB"
        n /= 1024.0
    return f"{n:.0f} B"


# --- Route

@router.get("", response_model=list[schemas.DocItem])
def get_documents(request: Request):
    base = str(request.base_url).rstrip("/")
    docs = []

    if not os.path.isdir(STATIC_DIR):
        return []

    for file in os.listdir(STATIC_DIR):
        path = os.path.join(STATIC_DIR, file)
        if not os.path.isfile(path):
            continue
        ext = file.split(".")[-1].lower() if "." in file else "unknown"
        size_label = f"{_human_size(os.path.getsize(path))} • {ext.upper()}"
        url = f"{base}/static/{quote(file)}"
        docs.append({"name": file, "url": url, "type": ext, "size_label": size_label})
    return docs