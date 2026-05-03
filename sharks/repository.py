from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from sharks.db import get_connection
from sharks.schemas import StudentProfile


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def save_event(whatsapp_id: str, role: str, message: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO conversation_events (whatsapp_id, role, message, created_at) VALUES (?, ?, ?, ?)",
            (whatsapp_id, role, message, utcnow()),
        )


def save_profile(profile: StudentProfile) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO student_profiles
            (whatsapp_id, name, email, marks, budget, target_country, target_course, work_experience, family_income, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                profile.whatsapp_id,
                profile.name,
                profile.email,
                profile.marks,
                profile.budget,
                profile.target_country,
                profile.target_course,
                profile.work_experience,
                profile.family_income,
                utcnow(),
            ),
        )


def save_document(whatsapp_id: str, document_type: str, raw_text: str | None, extracted: dict[str, Any]) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO document_records (whatsapp_id, document_type, raw_text, extracted_json, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (whatsapp_id, document_type, raw_text, json.dumps(extracted), utcnow()),
        )


def latest_profile(whatsapp_id: str) -> StudentProfile | None:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT * FROM student_profiles
            WHERE whatsapp_id = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (whatsapp_id,),
        ).fetchone()
    if not row:
        return None
    return StudentProfile(
        whatsapp_id=row["whatsapp_id"],
        name=row["name"],
        email=row["email"],
        marks=row["marks"],
        budget=row["budget"],
        target_country=row["target_country"],
        target_course=row["target_course"],
        work_experience=row["work_experience"],
        family_income=row["family_income"],
    )
