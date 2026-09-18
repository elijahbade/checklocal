import os
import sys
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.config import settings
from app.db import init_db, SessionLocal
from app.services.seed_data import seed_database_if_empty
from app.routes import webhook, reports, trending

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables
    init_db()
    # Seed sample verified data for Nigeria, Kenya, South Africa
    with SessionLocal() as db:
        seed_database_if_empty(db)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="CheckLocal - WhatsApp-First Civic Fact-Checking Platform for the OSF x Andela Hackathon ('Information you can trust')",
    lifespan=lifespan
)

# Enable CORS for local testing and external web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Backend API Routers
app.include_router(webhook.router)
app.include_router(reports.router)
app.include_router(trending.router)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "ai_engine": "Gemini 3.7 Flash + Regional Civic Heuristics"
    }

# Mount Frontend static files
frontend_dir = Path(__file__).resolve().parent.parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

    @app.get("/")
    def serve_frontend_index():
        index_file = frontend_dir / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return {"message": "Frontend index.html not found"}
