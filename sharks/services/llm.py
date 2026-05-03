from __future__ import annotations

from typing import Any

import httpx

from sharks.config import settings
from sharks.repository import latest_profile
from sharks.schemas import StudentProfile


def fallback_mentor_reply(message: str, profile: StudentProfile | None = None) -> str:
    text = message.lower()
    if any(word in text for word in ["loan", "finance", "emi", "funding"]):
        return "I can help with loan eligibility, offers, EMI planning, and document checklist. Share your marks and budget to get started."
    if any(word in text for word in ["visa", "interview", "docs"]):
        return "For visa and document help, I can generate a checklist and timeline. Share your target country for a tailored plan."
    if any(word in text for word in ["course", "country", "university", "masters", "pg"]):
        return "I can recommend best-fit countries, universities, and courses. Send marks, budget, and preferred field."
    if profile and profile.target_country:
        return f"Based on your profile, {profile.target_country.title()} looks like a strong starting point. I can refine it further with your marks and budget."
    return "I am your student mentor. Send your marks, budget, target country, or course field, and I will guide you step by step."


async def gemini_chat(message: str, profile: StudentProfile | None = None) -> tuple[str, str]:
    if not settings.llm_api_key:
        return fallback_mentor_reply(message, profile), "fallback"

    profile_hint = ""
    if profile:
        profile_hint = (
            f"Profile: marks={profile.marks}, budget={profile.budget}, country={profile.target_country}, course={profile.target_course}."
        )
    prompt = (
        "You are an AI student mentor for Indian students planning higher studies. "
        "Give concise, practical advice with one next step. "
        f"{profile_hint}\nUser message: {message}"
    )
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.llm_model}:generateContent?key={settings.llm_api_key}"
    payload: dict[str, Any] = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.5, "maxOutputTokens": 250},
    }
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPError:
        return fallback_mentor_reply(message, profile), "fallback"
    candidates = data.get("candidates", [])
    if not candidates:
        return fallback_mentor_reply(message, profile), "fallback"
    parts = candidates[0].get("content", {}).get("parts", [])
    texts = [part.get("text", "") for part in parts if isinstance(part, dict)]
    reply = " ".join(texts).strip()
    if reply:
        return reply, "llm"
    return fallback_mentor_reply(message, profile), "fallback"


async def mentor_reply(whatsapp_id: str, message: str) -> tuple[str, str]:
    profile = latest_profile(whatsapp_id)
    return await gemini_chat(message, profile)
