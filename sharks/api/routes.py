from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from sharks.repository import save_document, save_profile, save_event
from sharks.schemas import DocumentIn, LoanIn, MentorIn, ProfileIn, RoiIn, ScoringIn, StudentProfile
from sharks.services.admissions import admission_probability
from sharks.services.documents import parse_document_text
from sharks.services.llm import mentor_reply
from sharks.services.loans import loan_eligibility
from sharks.services.recommendations import recommend_options
from sharks.services.roi import roi_estimate

router = APIRouter()


@router.get("/")
def root() -> dict[str, Any]:
    from sharks.config import settings

    return {
        "name": settings.app_title,
        "version": settings.app_version,
        "base_url": settings.app_base_url,
        "stack": {
            "whatsapp": "Meta WhatsApp Cloud API",
            "llm": "Google Gemini API",
            "database": "SQLite now, Postgres later",
            "ocr": "optional later",
        },
    }


@router.get("/health")
def health() -> dict[str, str]:
    from sharks.repository import utcnow

    return {"status": "ok", "time": utcnow()}


@router.post("/api/profile")
def create_profile(payload: ProfileIn) -> dict[str, Any]:
    profile = StudentProfile(**payload.model_dump())
    save_profile(profile)
    return {
        "status": "saved",
        "profile": payload.model_dump(),
        "recommendations": recommend_options(profile),
        "admission": admission_probability(profile),
    }


@router.post("/api/mentor")
async def mentor(payload: MentorIn) -> dict[str, Any]:
    save_event(payload.whatsapp_id, "user", payload.message)
    reply, mode = await mentor_reply(payload.whatsapp_id, payload.message)
    save_event(payload.whatsapp_id, "assistant", reply)
    return {"reply": reply, "mode": mode}


@router.post("/api/recommend")
def recommend(payload: ProfileIn) -> dict[str, Any]:
    return {"recommendations": recommend_options(StudentProfile(**payload.model_dump()))}


@router.post("/api/admission-score")
def score(payload: ScoringIn) -> dict[str, Any]:
    profile = StudentProfile(
        whatsapp_id="demo",
        marks=payload.marks,
        budget=payload.budget,
        target_country=payload.target_country,
        target_course=payload.target_course,
        work_experience=payload.work_experience,
    )
    return admission_probability(profile)


@router.post("/api/roi")
def roi(payload: RoiIn) -> dict[str, Any]:
    return roi_estimate(payload)


@router.post("/api/loan-eligibility")
def loan(payload: LoanIn) -> dict[str, Any]:
    return loan_eligibility(payload)


@router.post("/api/documents/process")
def process_document(payload: DocumentIn) -> dict[str, Any]:
    parsed = parse_document_text(payload.raw_text)
    save_document(payload.whatsapp_id, payload.document_type, payload.raw_text, parsed)
    return {"status": "processed", "document_type": payload.document_type, "parsed": parsed}
