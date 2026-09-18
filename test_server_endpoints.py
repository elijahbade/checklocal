import sys
from pathlib import Path

# Configure UTF-8 for console output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

backend_dir = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(backend_dir))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def run_tests():
    print("=" * 60)
    print("🧪 Running End-to-End Test Suite for CheckLocal")
    print("=" * 60)

    # 1. Health Check
    print("\n[1] Testing GET /health...")
    res = client.get("/health")
    assert res.status_code == 200, f"Health check failed: {res.status_code}"
    data = res.json()
    print(f"  ✓ Health Status: {data.get('status')} | AI Engine: {data.get('ai_engine')}")

    # 2. Trending Facts Feed
    print("\n[2] Testing GET /api/trending...")
    res = client.get("/api/trending")
    assert res.status_code == 200
    facts = res.json()
    print(f"  ✓ Total Trending Facts returned: {len(facts)}")
    assert len(facts) > 0, "Expected trending facts in feed"
    print(f"  ✓ Sample Fact Title: '{facts[0]['title']}' ({facts[0]['country']})")

    # 3. Country Filter
    print("\n[3] Testing Country Filter (Kenya)...")
    res_ke = client.get("/api/trending?country=Kenya")
    assert res_ke.status_code == 200
    ke_facts = res_ke.json()
    print(f"  ✓ Kenya Facts returned: {len(ke_facts)}")
    assert all("Kenya" in f["country"] for f in ke_facts)

    # 4. WhatsApp Chat Simulation
    print("\n[4] Testing POST /api/simulate-chat...")
    payload = {
        "user_id": "+2348011223344",
        "message": "What is the petrol price in Ikeja right now?",
        "media_type": "text"
    }
    res_chat = client.post("/api/simulate-chat", json=payload)
    assert res_chat.status_code == 200
    chat_data = res_chat.json()
    print("  ✓ Bot Reply Received:")
    print("  " + "\n  ".join(chat_data["reply"].split("\n")[:8]) + "\n  ...")
    assert "CheckLocal" in chat_data["reply"]
    assert "In Nigerian Pidgin:" in chat_data["reply"]
    assert "Coming soon: Local Ambassador programme" in chat_data["reply"]
    assert chat_data["points_earned"] > 0
    print(f"  ✓ Points Awarded: +{chat_data['points_earned']} pts | Badge: {chat_data['user_badge']}")

    # 5. Web Report Submission
    print("\n[5] Testing POST /api/reports/submit...")
    report_payload = {
        "user_id": "citizen_tester",
        "country": "Nigeria",
        "location": "Lekki Phase 1, Lagos",
        "category": "fuel_price",
        "content": "Conoil at Lekki gate is selling fuel at ₦870 per litre with short queue of 4 cars.",
        "source": "web"
    }
    res_rep = client.post("/api/reports/submit", json=report_payload)
    assert res_rep.status_code == 200
    rep_data = res_rep.json()
    print(f"  ✓ Report Verified! Category: {rep_data['category']} | Confidence: {rep_data['confidence_level']}")
    print(f"  ✓ Pidgin Summary: {rep_data['verified_summary_pidgin']}")
    print(f"  ✓ Next Action: {rep_data['next_action']}")

    # 6. Twilio WhatsApp Webhook
    print("\n[6] Testing POST /api/webhook/twilio (TwiML Response)...")
    webhook_form = {
        "From": "whatsapp:+2348099887766",
        "Body": "Is power out in Surulere?"
    }
    res_tw = client.post("/api/webhook/twilio", data=webhook_form)
    assert res_tw.status_code == 200
    assert "application/xml" in res_tw.headers.get("content-type", "")
    assert "<Response>" in res_tw.text
    assert "<Message>" in res_tw.text
    print("  ✓ Valid TwiML XML returned successfully for Twilio WhatsApp!")

    # 7. Frontend Static Mounting
    print("\n[7] Testing GET / (Frontend Landing Mirror)...")
    res_ui = client.get("/")
    assert res_ui.status_code == 200
    assert "CheckLocal" in res_ui.text
    assert "WhatsApp Simulator" in res_ui.text
    print("  ✓ Public web mirror loaded successfully!")

    print("\n" + "=" * 60)
    print("🎉 ALL 7 END-TO-END TESTS PASSED WITH 100% SUCCESS!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
