from __future__ import annotations

from typing import Any

import httpx
from fastapi import HTTPException, Query

from sharks.config import settings
from sharks.repository import latest_profile, save_event
from sharks.schemas import LoanIn
from sharks.services.loans import loan_eligibility
from sharks.services.recommendations import recommend_options


def extract_whatsapp_payload(payload: dict[str, Any]) -> tuple[str | None, str | None]:
    entry = payload.get("entry", [])
    if not entry:
        return None, None
    changes = entry[0].get("changes", [])
    if not changes:
        return None, None
    value = changes[0].get("value", {})
    messages = value.get("messages", [])
    contacts = value.get("contacts", [])
    sender = contacts[0].get("wa_id") if contacts else None
    message_text = None
    if messages:
        message = messages[0]
        message_text = message.get("text", {}).get("body") or message.get("type", "")
    return sender, message_text


async def send_whatsapp_message(to: str, text: str) -> dict[str, Any]:
    if not settings.whatsapp_api_token or not settings.whatsapp_phone_number_id:
        return {"status": "simulated", "to": to, "text": text}

    url = f"https://graph.facebook.com/v19.0/{settings.whatsapp_phone_number_id}/messages"
    headers = {"Authorization": f"Bearer {settings.whatsapp_api_token}", "Content-Type": "application/json"}
    payload = {"messaging_product": "whatsapp", "to": to, "type": "text", "text": {"body": text}}
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()


def route_user_message(sender: str, message: str) -> str:
    lower = message.lower().strip()
    profile = latest_profile(sender)

    if any(keyword in lower for keyword in ["start", "hi", "hello", "menu"]):
        return (
            "Welcome to Sharks. Send your marks, budget, preferred country, and course field. "
            "I can then recommend options, score admission chances, and estimate loan support."
        )

    if any(keyword in lower for keyword in ["recommend", "country", "course", "university"]):
        if not profile:
            return "Share your marks and budget first so I can recommend countries and courses."
        result = recommend_options(profile)
        return (
            f"Best-fit countries: {', '.join(result['countries'])}. "
            f"Suggested courses: {', '.join(result['courses'])}. "
            f"University tier: {result['university_tier']}."
        )

    if any(keyword in lower for keyword in ["loan", "emi", "finance", "funding"]):
        if not profile or profile.family_income is None or profile.budget is None or profile.marks is None:
            return "To estimate loan eligibility, share marks, budget, and family income."
        result = loan_eligibility(
            LoanIn(
                whatsapp_id=sender,
                marks=profile.marks,
                family_income=profile.family_income,
                budget=profile.budget,
                target_country=profile.target_country,
                target_course=profile.target_course,
            )
        )
        if result["offers"]:
            offer_text = "; ".join([f"{item['name']} up to {item['loan_amount']}" for item in result["offers"]])
            return f"Loan status: {result['status']}. Offers: {offer_text}."
        return f"Loan status: {result['status']}. I will need stronger profile details for offers."

    if any(keyword in lower for keyword in ["roi", "salary", "return"]):
        return "Send course, country, tuition cost, living cost, and duration so I can calculate ROI and payback period."

    return "Got it. I can help with admissions, ROI, loans, and documents. Try sending your profile details or ask a specific question."


async def handle_whatsapp_message(sender: str, message: str) -> str:
    save_event(sender, "user", message)
    reply = route_user_message(sender, message)
    save_event(sender, "assistant", reply)
    return reply


async def process_whatsapp_payload(payload: dict[str, Any]) -> dict[str, Any]:
    sender, message = extract_whatsapp_payload(payload)
    if not sender or not message:
        return {"status": "ignored"}
    reply = await handle_whatsapp_message(sender, message)
    return {"status": "processed", "sender": sender, "reply": reply}


def verify_webhook(
    mode: str | None = Query(default=None, alias="hub.mode"),
    challenge: str | None = Query(default=None, alias="hub.challenge"),
    verify_token: str | None = Query(default=None, alias="hub.verify_token"),
) -> str:
    token = verify_token or ""
    if mode == "subscribe" and token == settings.whatsapp_verify_token:
        return challenge or ""
    raise HTTPException(status_code=403, detail="Verification failed")
