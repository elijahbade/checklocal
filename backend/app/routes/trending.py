from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.db import get_db
from app.models import TrendingFactModel, ChatSimulationRequest, BenchmarkModel
from app.services.ai_service import ai_service
from app.services.points_service import award_points

router = APIRouter(prefix="/api", tags=["trending"])

@router.get("/trending")
def get_trending_facts(
    country: Optional[str] = Query(None, description="Filter by country: Nigeria, Kenya, South Africa, or all"),
    category: Optional[str] = Query(None, description="Filter by category: fuel_price, food_staple, power_status, water_status, rumor_claim, or all"),
    search: Optional[str] = Query(None, description="Search keyword in title, location, or summary"),
    db: Session = Depends(get_db)
):
    """
    Public feed of trending verified local facts.
    Supports country switching (Nigeria, Kenya, South Africa) and category filtering.
    """
    query = db.query(TrendingFactModel)

    if country and country.lower() != "all":
        query = query.filter(TrendingFactModel.country.ilike(f"%{country}%"))

    if category and category.lower() != "all":
        query = query.filter(TrendingFactModel.category == category)

    if search and search.strip():
        term = f"%{search.strip()}%"
        query = query.filter(
            (TrendingFactModel.title.ilike(term)) |
            (TrendingFactModel.location.ilike(term)) |
            (TrendingFactModel.summary_en.ilike(term)) |
            (TrendingFactModel.summary_pidgin.ilike(term))
        )

    facts = query.order_by(TrendingFactModel.is_hot.desc(), TrendingFactModel.updated_at.desc()).all()

    return [
        {
            "id": f.id,
            "title": f.title,
            "country": f.country,
            "location": f.location,
            "category": f.category,
            "summary_en": f.summary_en,
            "summary_pidgin": f.summary_pidgin or "",
            "summary_swahili": f.summary_swahili or "",
            "summary_yoruba": f.summary_yoruba or "",
            "summary_hausa": f.summary_hausa or "",
            "summary_zulu": f.summary_zulu or "",
            "confidence_level": f.confidence_level,
            "sources": f.sources,
            "action": f.action,
            "report_count": f.report_count,
            "upvotes": f.upvotes,
            "is_hot": f.is_hot,
            # PowerWatch Feeder Attributes
            "feeder_name": getattr(f, "feeder_name", None),
            "disco_name": getattr(f, "disco_name", None),
            "tariff_band": getattr(f, "tariff_band", None),
            "promised_hours": getattr(f, "promised_hours", None),
            "actual_hours_avg": getattr(f, "actual_hours_avg", None),
            "overbilling_differential": getattr(f, "overbilling_differential", None),
            "docket_ready": getattr(f, "docket_ready", False) or (f.category == "power_status"),
            "docket_number": getattr(f, "docket_number", None),
            "escalation_target": "NERC Regulatory Forum / NERSA" if f.category == "power_status" else ("NMDPRA Enforcement" if f.category == "fuel_price" else ("FCCPC Anti-Gouging" if f.category == "food_staple" else "Civil Society FactCheck Wire")),
            "updated_at": f.updated_at.strftime("%b %d, %Y • %I:%M %p")
        }
        for f in facts
    ]

@router.get("/trending/{fact_id}/docket")
def get_feeder_docket(fact_id: int, db: Session = Depends(get_db)):
    """
    Generates a formal legal petition and regulatory dispute docket
    ready for submission to NERC Forum Office (Nigeria) or NERSA (South Africa).
    """
    from app.services.docket_service import docket_service
    docket = docket_service.generate_docket_for_fact(fact_id, db)
    if not docket:
        raise HTTPException(status_code=404, detail="Dispute docket not found for this record")
    return docket

@router.get("/trending/{fact_id}/docket/download")
def download_feeder_docket(fact_id: int, db: Session = Depends(get_db)):
    """Downloads the formal regulatory petition as a clean markdown/text document."""
    from fastapi.responses import Response
    from app.services.docket_service import docket_service
    docket = docket_service.generate_docket_for_fact(fact_id, db)
    if not docket:
        raise HTTPException(status_code=404, detail="Dispute docket not found")
        
    filename = f"PowerWatch_Petition_{docket['docket_reference'].replace('/', '_')}.md"
    return Response(
        content=docket["markdown_petition"],
        media_type="text/markdown",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )

@router.post("/trending/{fact_id}/upvote")
def upvote_trending_fact(fact_id: int, db: Session = Depends(get_db)):
    """Allows citizens to confirm/upvote a fact card."""
    fact = db.query(TrendingFactModel).filter(TrendingFactModel.id == fact_id).first()
    if not fact:
        raise HTTPException(status_code=404, detail="Fact card not found")
    fact.upvotes += 1
    db.commit()
    return {"status": "success", "upvotes": fact.upvotes}

@router.get("/tweets/recent")
def get_recent_tweets():
    """Returns real-time automated tweets syndicated by CheckLocal to X."""
    from app.services.twitter_service import twitter_service
    return twitter_service.get_recent_tweets()

@router.post("/trending/{fact_id}/tweet")
def syndicate_fact_to_twitter(fact_id: int, db: Session = Depends(get_db)):
    """Automatically composes and publishes a verified fact to X (Twitter)."""
    from app.services.twitter_service import twitter_service
    fact = db.query(TrendingFactModel).filter(TrendingFactModel.id == fact_id).first()
    if not fact:
        raise HTTPException(status_code=404, detail="Fact not found")
    
    fact_dict = {
        "id": fact.id,
        "category": fact.category,
        "country": fact.country,
        "location": fact.location,
        "summary_en": fact.summary_en,
        "action": fact.action
    }
    tweet_result = twitter_service.publish_tweet(fact_dict)
    return {"status": "success", "tweet": tweet_result}

@router.get("/benchmarks")
def get_benchmarks(country: Optional[str] = "Nigeria", db: Session = Depends(get_db)):
    """Returns official regulatory benchmarks and hotlines for the selected country."""
    query = db.query(BenchmarkModel)
    if country and country.lower() != "all":
        query = query.filter(BenchmarkModel.country.ilike(f"%{country}%"))
    benchmarks = query.all()
    return [
        {
            "id": b.id,
            "country": b.country,
            "category": b.category,
            "item_name": b.item_name,
            "official_rate": b.official_rate,
            "official_source": b.official_source,
            "hotline_contact": b.hotline_contact
        }
        for b in benchmarks
    ]

from app.config import settings

@router.get("/engine-status")
def get_engine_status():
    """
    Returns whether Google Gemini AI or the Civic Heuristic Fallback Engine is active.
    """
    is_gemini = bool(ai_service.client)
    engine_name = f"Google Gemini ({settings.GEMINI_MODEL})" if is_gemini else "Civic Heuristic Fallback Engine"
    return {
        "engine": engine_name,
        "is_gemini": is_gemini,
        "model": settings.GEMINI_MODEL if is_gemini else "heuristics",
        "has_gemini_key": bool(settings.GEMINI_API_KEY)
    }

@router.post("/simulate-chat")
async def simulate_whatsapp_chat(payload: ChatSimulationRequest, db: Session = Depends(get_db)):
    """
    Direct endpoint for the interactive WhatsApp phone simulator.
    Powers real-time interactive testing for hackathon judges and citizens directly in browser.
    """
    sender_id = payload.user_id or "+2348012345678"
    msg_text = payload.message.strip()

    if not msg_text:
        return {
            "reply": "👋 *Welcome to CheckLocal WhatsApp Fact-Check!*\n\nForward any price claim, power status, or rumor. For example:\n• _Fuel price in Ikeja_\n• _Current price of Garri in Mile 12_\n• _Power outage in Lekki_\n• _Is petrol dropping to ₦450?_\n\n_Coming soon: Local Ambassador programme + other civic tools._",
            "points_earned": 0,
            "total_points": 0,
            "badge": "Civic Scout"
        }

    # Run AI verification
    verification = await ai_service.verify_report(
        text=msg_text,
        user_id=sender_id,
        media_type=payload.media_type or "text"
    )

    points_earned = 15 if verification.get("confidence_level") == "Verified" else 10
    total_points, user_badge = award_points(db, sender_id, points_earned)

    # Format WhatsApp text
    formatted_reply = ai_service.format_whatsapp_reply(
        data=verification,
        user_points=total_points,
        points_earned=points_earned,
        user_badge=user_badge
    )

    return {
        "reply": formatted_reply,
        "engine": verification.get("engine", "Civic Engine"),
        "verification_data": verification,
        "points_earned": points_earned,
        "total_points": total_points,
        "user_badge": user_badge,
        "timestamp": datetime.utcnow().strftime("%I:%M %p")
    }
