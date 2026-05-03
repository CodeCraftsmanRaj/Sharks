from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard() -> str:
    html_path = Path(__file__).resolve().parent.parent / "web" / "index.html"
    return html_path.read_text(encoding="utf-8")
