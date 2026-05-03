from __future__ import annotations

from fastapi import FastAPI

from sharks.api.routes import router as core_router
from sharks.api.whatsapp import router as whatsapp_router
from sharks.config import settings
from sharks.db import init_db


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_title, version=settings.app_version)
    app.include_router(core_router)
    app.include_router(whatsapp_router)

    @app.on_event("startup")
    def startup_event() -> None:
        init_db()

    return app


app = create_app()
