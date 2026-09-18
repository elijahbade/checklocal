import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(backend_dir))

# Configure UTF-8 for console output on Windows (supports Naira symbol and emojis)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.db import init_db, SessionLocal
from app.services.seed_data import seed_database_if_empty
from app.models import TrendingFactModel, BenchmarkModel
from app.services.ai_service import ai_service
import asyncio

async def test_backend():
    print("Testing DB Init...")
    init_db()
    with SessionLocal() as db:
        seed_database_if_empty(db)
        count = db.query(TrendingFactModel).count()
        bench_count = db.query(BenchmarkModel).count()
        print(f"DB initialized! Trending facts: {count}, Benchmarks: {bench_count}")
        assert count > 0, "No facts seeded"
        assert bench_count > 0, "No benchmarks seeded"

    print("Testing AI Verification Heuristic Engine...")
    test_queries = [
        ("What is fuel price in Ikeja today?", "Nigeria"),
        ("How much is paint bucket of garri in Mile 12?", "Nigeria"),
        ("Is there load shedding in Johannesburg?", "South Africa"),
        ("I heard a voice note that petrol is dropping to 450 naira tomorrow", "Nigeria")
    ]

    for q, country in test_queries:
        res = await ai_service.verify_report(text=q, user_id="test_user")
        print(f"\nQuery: '{q}'")
        print(f"Category: {res.get('category')} | Confidence: {res.get('confidence_level')} ({res.get('confidence_score')}%)")
        print(f"EN Summary: {res.get('verified_summary_en')}")
        print(f"Pidgin Summary: {res.get('verified_summary_pidgin')}")
        print(f"Next Action: {res.get('next_action')}")
        
    print("\n✅ All Backend Core Tests Passed Successfully!")

if __name__ == "__main__":
    asyncio.run(test_backend())
