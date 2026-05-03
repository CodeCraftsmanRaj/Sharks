from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_title: str = "Sharks"
    app_version: str = "0.1.0"
    whatsapp_api_token: str = os.getenv("WHATSAPP_API_TOKEN", "")
    whatsapp_phone_number_id: str = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
    whatsapp_verify_token: str = os.getenv("WHATSAPP_VERIFY_TOKEN", "")
    whatsapp_app_secret: str = os.getenv("WHATSAPP_APP_SECRET", "")
    llm_api_key: str = os.getenv("LLM_API_KEY", "")
    llm_model: str = os.getenv("LLM_MODEL", "gemini-2.0-flash")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./sharks.db")
    app_base_url: str = os.getenv("APP_BASE_URL", "http://127.0.0.1:8000")


settings = Settings()
