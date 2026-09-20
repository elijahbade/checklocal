import os
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv

# Load .env if present
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseModel):
    PROJECT_NAME: str = "CheckLocal"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # AI Config (Google Gemini)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    GEMINI_FALLBACK_MODEL: str = "gemini-1.5-flash"
    
    # WhatsApp Bot Profile
    WHATSAPP_BOT_NAME: str = "CheckLocal Verified Bot"
    WHATSAPP_DISPLAY_PHONE: str = os.getenv("WHATSAPP_DISPLAY_PHONE", "+234 812 CHECK-99")
    WHATSAPP_LINK: str = os.getenv("WHATSAPP_LINK", "https://wa.me/2348122432599?text=Hello%20CheckLocal,%20I%20want%20to%20verify%20a%20report")
    
    # Twilio Integration
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_WHATSAPP_NUMBER: str = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")
    
    # Meta WhatsApp Cloud API Integration
    META_VERIFY_TOKEN: str = os.getenv("META_VERIFY_TOKEN", "checklocal_verify_token_2026")
    META_WHATSAPP_TOKEN: str = os.getenv("META_WHATSAPP_TOKEN", "")
    
    # Database Config
    DATABASE_PATH: Path = Path(__file__).resolve().parent.parent / "checklocal.db"
    DATABASE_URL: str = f"sqlite:///{DATABASE_PATH}"

settings = Settings()
