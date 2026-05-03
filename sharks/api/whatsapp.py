from __future__ import annotations

from fastapi import APIRouter, BackgroundTasks, Query, Request
from fastapi.responses import PlainTextResponse

from sharks.services.whatsapp import process_whatsapp_payload, send_whatsapp_message, verify_webhook

router = APIRouter()


@router.get("/webhook/whatsapp", response_class=PlainTextResponse)
def verify(
    mode: str | None = Query(default=None, alias="hub.mode"),
    challenge: str | None = Query(default=None, alias="hub.challenge"),
    verify_token: str | None = Query(default=None, alias="hub.verify_token"),
) -> str:
    return verify_webhook(mode=mode, challenge=challenge, verify_token=verify_token)


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
