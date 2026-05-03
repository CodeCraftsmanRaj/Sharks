from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from sharks.api.frontend import router as frontend_router
from sharks.api.routes import router as core_router
from sharks.api.whatsapp import router as whatsapp_router
from sharks.config import settings
from sharks.db import init_db


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_title, version=settings.app_version)
    app.include_router(core_router)
    app.include_router(whatsapp_router)
    app.include_router(frontend_router)

    static_dir = Path(__file__).resolve().parent / "web" / "static"
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    @app.on_event("startup")
    def startup_event() -> None:
        init_db()

    return app


app = create_app()
