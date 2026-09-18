from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# SQLAlchemy ORM Models
class ReportModel(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    source = Column(String(50), default="whatsapp")  # whatsapp, web, simulator
    user_id = Column(String(100), index=True)        # Phone number or session hash
    country = Column(String(50), default="Nigeria")  # Nigeria, Kenya, South Africa
    location = Column(String(150), default="Unknown")
    category = Column(String(50), default="rumor_claim") # fuel_price, food_staple, power_status, water_status, rumor_claim
    raw_content = Column(Text, nullable=False)
    media_type = Column(String(50), default="text")  # text, voice_note, screenshot
    
    # Verification and AI analysis
    status = Column(String(50), default="verified")  # verified, high_confidence, community_consensus, investigating, disputed
    confidence_level = Column(String(50), default="High")  # High, Medium, Low, Unverified
    confidence_score = Column(Integer, default=85)          # 0 - 100
    verified_summary_en = Column(Text, nullable=True)
    verified_summary_pidgin = Column(Text, nullable=True)
    verified_summary_swahili = Column(Text, nullable=True)
    verified_summary_yoruba = Column(Text, nullable=True)
    verified_summary_hausa = Column(Text, nullable=True)
    verified_summary_zulu = Column(Text, nullable=True)
    detected_language = Column(String(50), default="English")
    sources = Column(Text, nullable=True)
    next_action = Column(Text, nullable=True)
    points_awarded = Column(Integer, default=10)
    
    # PowerWatch Evidentiary Fields
    meter_number = Column(String(50), nullable=True)
    disco_name = Column(String(100), nullable=True)
    feeder_name = Column(String(150), nullable=True)
    tariff_band = Column(String(50), nullable=True)
    hours_supplied = Column(String(50), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class TrendingFactModel(Base):
    __tablename__ = "trending_facts"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    country = Column(String(50), default="Nigeria")
    location = Column(String(150), nullable=False)
    category = Column(String(50), nullable=False)
    summary_en = Column(Text, nullable=False)
    summary_pidgin = Column(Text, nullable=True)
    summary_swahili = Column(Text, nullable=True)
    summary_yoruba = Column(Text, nullable=True)
    summary_hausa = Column(Text, nullable=True)
    summary_zulu = Column(Text, nullable=True)
    confidence_level = Column(String(50), default="High")
    sources = Column(Text, nullable=False)
    action = Column(Text, nullable=False)
    report_count = Column(Integer, default=1)
    upvotes = Column(Integer, default=0)
    is_hot = Column(Boolean, default=True)
    
    # PowerWatch Feeder Audit & Dispute Docket Attributes
    feeder_name = Column(String(150), nullable=True)
    disco_name = Column(String(100), nullable=True)
    tariff_band = Column(String(50), nullable=True)
    promised_hours = Column(String(50), nullable=True)
    actual_hours_avg = Column(String(50), nullable=True)
    overbilling_differential = Column(String(100), nullable=True)
    docket_ready = Column(Boolean, default=False)
    docket_number = Column(String(100), nullable=True)
    
    updated_at = Column(DateTime, default=datetime.utcnow)

class UserProfileModel(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(100), unique=True, index=True)
    display_name = Column(String(100), default="Citizen Reporter")
    total_points = Column(Integer, default=0)
    reports_count = Column(Integer, default=0)
    badge = Column(String(50), default="Civic Scout")
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)

class BenchmarkModel(Base):
    __tablename__ = "benchmarks"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    country = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False)
    item_name = Column(String(150), nullable=False)
    official_rate = Column(String(150), nullable=False)
    official_source = Column(String(200), nullable=False)
    hotline_contact = Column(String(200), nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow)

# Pydantic Schemas for API requests & responses
class ReportCreateRequest(BaseModel):
    user_id: Optional[str] = "web_citizen"
    country: Optional[str] = "Nigeria"
    location: Optional[str] = "Lagos, Ikeja"
    category: Optional[str] = "fuel_price"
    content: str
    media_type: Optional[str] = "text"
    source: Optional[str] = "web"

class VerifyResponse(BaseModel):
    category: str
    location: str
    country: str
    verified_summary_en: str
    verified_summary_pidgin: str
    verified_summary_swahili: Optional[str] = None
    verified_summary_yoruba: Optional[str] = None
    verified_summary_hausa: Optional[str] = None
    verified_summary_zulu: Optional[str] = None
    detected_language: Optional[str] = "English"
    confidence_level: str
    confidence_score: int
    sources: List[str]
    next_action: str
    points_awarded: int
    user_total_points: int
    user_badge: str
    whatsapp_formatted_text: str
    coming_soon_note: str = "Coming soon: Local Ambassador programme + other civic tools."

class TrendingFactItem(BaseModel):
    id: int
    title: str
    country: str
    location: str
    category: str
    summary_en: str
    summary_pidgin: Optional[str] = None
    confidence_level: str
    sources: str
    action: str
    report_count: int
    upvotes: int
    is_hot: bool
    updated_at: str

class ChatSimulationRequest(BaseModel):
    user_id: Optional[str] = "+2348012345678"
    message: str
    media_type: Optional[str] = "text"
    country: Optional[str] = "Nigeria"
