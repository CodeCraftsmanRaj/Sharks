from __future__ import annotations

from fastapi import APIRouter, BackgroundTasks, Request

from sharks.services.whatsapp import process_whatsapp_payload, send_whatsapp_message, verify_webhook

router = APIRouter()


@router.get("/webhook/whatsapp")
def verify() -> str:
    return verify_webhook()


@router.post("/webhook/whatsapp")
async def webhook(request: Request, background_tasks: BackgroundTasks) -> dict[str, object]:
    payload = await request.json()
    result = await process_whatsapp_payload(payload)
    if result.get("status") == "processed":
        background_tasks.add_task(send_whatsapp_message, result["sender"], result["reply"])
    return result


@router.post("/api/whatsapp/send")
async def send_message(payload: dict[str, str]) -> dict[str, object]:
    result = await send_whatsapp_message(payload["to"], payload["text"])
    return {"status": "sent", "result": result}
