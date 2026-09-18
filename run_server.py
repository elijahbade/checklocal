#!/usr/bin/env python
"""
CheckLocal - Local Server Runner
OSF x Andela Hackathon: 'Information you can trust'
"""
import sys
import os
from pathlib import Path

# Add backend directory to python path
backend_dir = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(backend_dir))

# Configure UTF-8 for console output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import uvicorn
from app.config import settings
from app.db import init_db, SessionLocal
from app.services.seed_data import seed_database_if_empty

def main():
    print("=" * 60)
    print("🚀 Starting CheckLocal Civic Fact-Checking Platform")
    print("=" * 60)
    print(f"• Project: {settings.PROJECT_NAME} v{settings.VERSION}")
    print(f"• Target Countries: Nigeria (Primary), Kenya, South Africa")
    print(f"• Environment: {settings.ENVIRONMENT}")
    print(f"• Database: {settings.DATABASE_PATH}")
    print(f"• WhatsApp Bot Number: {settings.WHATSAPP_DISPLAY_PHONE}")
    print("-" * 60)
    
    # Initialize DB and seed initial facts
    print("📦 Initializing database & seeding verified civic facts...")
    init_db()
    with SessionLocal() as db:
        seed_database_if_empty(db)
    print("✅ Database ready with verified regional data.")
    
    print("-" * 60)
    print("🌐 Web Mirror & Interactive WhatsApp Simulator: http://127.0.0.1:8000")
    print("📖 API Documentation (Swagger): http://127.0.0.1:8000/docs")
    print("⚡ Twilio WhatsApp Webhook: http://127.0.0.1:8000/api/webhook/twilio")
    print("⚡ Meta WhatsApp Webhook: http://127.0.0.1:8000/api/webhook/meta")
    print("=" * 60)
    
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)

if __name__ == "__main__":
    main()
