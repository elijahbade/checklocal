import json
import logging
from fastapi import APIRouter, Request, Response, Depends, Form
from sqlalchemy.orm import Session
import httpx

from app.config import settings
from app.db import get_db
from app.models import ReportModel, TrendingFactModel
from app.services.ai_service import ai_service
from app.services.points_service import award_points

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/webhook", tags=["webhooks"])

@router.post("/twilio")
async def twilio_whatsapp_webhook(
    request: Request,
    From: str = Form("whatsapp:+2348000000000"),
    Body: str = Form(""),
    MediaContentType0: str = Form(None),
    MediaUrl0: str = Form(None),
    db: Session = Depends(get_db)
):
    """
    Twilio WhatsApp Webhook Endpoint.
    Ingests user messages from WhatsApp, conducts AI civic verification,
    awards trust points, and returns immediate TwiML message response.
    """
    sender_phone = From.replace("whatsapp:", "").strip()
    user_text = Body.strip()
    
    media_type = "text"
    if MediaContentType0:
        if "audio" in MediaContentType0:
            media_type = "voice_note"
            if not user_text:
                user_text = "[Voice Note Report: Local price or service inquiry]"
        elif "image" in MediaContentType0:
            media_type = "screenshot"
            if not user_text:
                user_text = "[Screenshot Report: Circulating receipt or WhatsApp forward]"

    if not user_text:
        user_text = "Hello, I want to verify a report."

    # Perform AI verification
    verification = await ai_service.verify_report(
        text=user_text,
        user_id=sender_phone,
        media_type=media_type
    )

    # Award points
    points_earned = 15 if verification.get("confidence_level") == "Verified" else 10
    total_points, user_badge = award_points(db, sender_phone, points_earned)

    # Persist Report to database
    report = ReportModel(
        source="whatsapp",
        user_id=sender_phone,
        country=verification.get("country", "Nigeria"),
        location=verification.get("location", "Lagos, Nigeria"),
        category=verification.get("category", "rumor_claim"),
        raw_content=user_text,
        media_type=media_type,
        status="verified" if verification.get("confidence_level") in ["Verified", "High"] else "investigating",
        confidence_level=verification.get("confidence_level", "High"),
        confidence_score=verification.get("confidence_score", 85),
        verified_summary_en=verification.get("verified_summary_en", ""),
        verified_summary_pidgin=verification.get("verified_summary_pidgin", ""),
        sources=", ".join(verification.get("sources", [])),
        next_action=verification.get("next_action", ""),
        points_awarded=points_earned
    )
    db.add(report)
    db.commit()

    # Format reply adhering to hackathon requirements
    reply_body = ai_service.format_whatsapp_reply(
        data=verification,
        user_points=total_points,
        points_earned=points_earned,
        user_badge=user_badge
    )

    # Return standard TwiML XML
    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{reply_body}</Message>
</Response>"""

    return Response(content=twiml_response, media_type="application/xml")

@router.get("/meta")
async def meta_whatsapp_verify(request: Request):
    """
    Meta Cloud API Webhook Verification Endpoint.
    Used by Meta to verify webhook endpoint during setup.
    """
    params = request.query_params
    hub_mode = params.get("hub.mode")
    hub_token = params.get("hub.verify_token")
    hub_challenge = params.get("hub.challenge")

    if hub_mode == "subscribe" and hub_token == settings.META_VERIFY_TOKEN:
        logger.info("Meta Webhook verified successfully.")
        return Response(content=hub_challenge, media_type="text/plain")
    return Response(content="Verification token mismatch", status_code=403)

@router.post("/meta")
async def meta_whatsapp_message(request: Request, db: Session = Depends(get_db)):
    """
    Meta Cloud API Webhook Event Handler.
    Processes incoming messages from Meta WhatsApp Cloud API.
    """
    try:
        body = await request.json()
    except Exception:
        return {"status": "bad_request"}

    entry = body.get("entry", [])
    if not entry:
        return {"status": "no_entry"}

    changes = entry[0].get("changes", [])
    if not changes:
        return {"status": "no_changes"}

    value = changes[0].get("value", {})
    messages = value.get("messages", [])
    if not messages:
        return {"status": "no_messages"}

    msg = messages[0]
    sender_phone = msg.get("from")
    msg_type = msg.get("type", "text")
    
    text_content = ""
    if msg_type == "text":
        text_content = msg.get("text", {}).get("body", "")
    elif msg_type == "audio":
        text_content = "[Voice Note Report submitted via WhatsApp]"
    elif msg_type == "image":
        text_content = msg.get("image", {}).get("caption", "[Screenshot verification submitted]")
    else:
        text_content = f"[{msg_type} message received]"

    # Verify and award points
    verification = await ai_service.verify_report(text=text_content, user_id=sender_phone, media_type=msg_type)
    points_earned = 10
    total_points, user_badge = award_points(db, sender_phone, points_earned)

    # Save to database
    report = ReportModel(
        source="whatsapp_meta",
        user_id=sender_phone,
        country=verification.get("country", "Nigeria"),
        location=verification.get("location", "Lagos, Nigeria"),
        category=verification.get("category", "rumor_claim"),
        raw_content=text_content,
        media_type=msg_type,
        verified_summary_en=verification.get("verified_summary_en", ""),
        verified_summary_pidgin=verification.get("verified_summary_pidgin", ""),
        confidence_level=verification.get("confidence_level", "High"),
        confidence_score=verification.get("confidence_score", 85),
        sources=", ".join(verification.get("sources", [])),
        next_action=verification.get("next_action", ""),
        points_awarded=points_earned
    )
    db.add(report)
    db.commit()

    reply_body = ai_service.format_whatsapp_reply(verification, total_points, points_earned, user_badge)

    # If META_WHATSAPP_TOKEN is configured, send the message back via Meta Graph API
    if settings.META_WHATSAPP_TOKEN:
        phone_number_id = value.get("metadata", {}).get("phone_number_id")
        if phone_number_id:
            try:
                url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"
                headers = {
                    "Authorization": f"Bearer {settings.META_WHATSAPP_TOKEN}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "messaging_product": "whatsapp",
                    "to": sender_phone,
                    "type": "text",
                    "text": {"body": reply_body}
                }
                async with httpx.AsyncClient() as client:
                    await client.post(url, headers=headers, json=payload, timeout=10.0)
            except Exception as e:
                logger.error(f"Error dispatching Meta WhatsApp message: {e}")

    return {"status": "success", "user_points": total_points}
