import sys
from pathlib import Path

# Configure UTF-8 for console output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

backend_dir = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(backend_dir))

from fastapi.testclient import TestClient
from app.main import app
from app.db import init_db, SessionLocal
from app.services.seed_data import seed_database_if_empty

# Ensure DB is migrated and seeded with PowerWatch data
init_db()
with SessionLocal() as db:
    seed_database_if_empty(db, force_refresh=True)

client = TestClient(app)

def run_tests():
    print("=" * 60)
    print("🧪 Running End-to-End Test Suite for PowerWatch by CheckLocal")
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
    print(f"  ✓ Total Facts returned: {len(facts)}")
    assert len(facts) > 0, "Expected facts in feed"
    print(f"  ✓ Sample Fact Title: '{facts[0]['title']}' ({facts[0]['country']})")

    # 3. PowerWatch Feeder Audit Records
    print("\n[3] Testing PowerWatch Feeder Audits...")
    res_power = client.get("/api/trending?category=power_status")
    assert res_power.status_code == 200
    power_facts = res_power.json()
    print(f"  ✓ Feeder Audit records returned: {len(power_facts)}")
    assert len(power_facts) >= 3, "Expected at least 3 feeder audit records"
    sample_feeder = power_facts[0]
    print(f"  ✓ Feeder: {sample_feeder.get('feeder_name')}")
    print(f"  ✓ DisCo: {sample_feeder.get('disco_name')}")
    print(f"  ✓ Supply: {sample_feeder.get('actual_hours_avg')}h / {sample_feeder.get('promised_hours')}h statutory minimum")
    print(f"  ✓ Unlawful Differential: {sample_feeder.get('overbilling_differential')}")
    print(f"  ✓ Docket Number: {sample_feeder.get('docket_number')}")

    # 4. Regulatory Dispute Docket Generation & Download
    print("\n[4] Testing Regulatory Dispute Docket Generator (NERC / NERSA)...")
    feeder_id = sample_feeder["id"]
    res_docket = client.get(f"/api/trending/{feeder_id}/docket")
    assert res_docket.status_code == 200
    docket_data = res_docket.json()
    print(f"  ✓ Docket Reference: {docket_data['docket_reference']}")
    print(f"  ✓ Regulatory Body: {docket_data['regulatory_body']}")
    print(f"  ✓ Statutory Basis: {docket_data['statutory_basis']}")
    assert "Section 63" in docket_data["statutory_basis"] or "Pretoria High Court" in docket_data["statutory_basis"]
    assert len(docket_data["sample_meters"]) > 0
    print(f"  ✓ Corroborated Sample Meters: {len(docket_data['sample_meters'])}")
    
    # Test Docket Download Endpoint
    res_dl = client.get(f"/api/trending/{feeder_id}/docket/download")
    assert res_dl.status_code == 200
    assert "attachment" in res_dl.headers.get("content-disposition", "")
    assert "OFFICIAL REGULATORY" in res_dl.text or "FORMAL REGULATORY" in res_dl.text
    print("  ✓ Markdown petition document generated and downloaded successfully!")

    # 5. WhatsApp Chat Simulation (Power Outage & Meter Logging)
    print("\n[5] Testing POST /api/simulate-chat (Meter Logging & Tariff Breach)...")
    payload = {
        "user_id": "+2348011223344",
        "message": "Magodo Phase 2 Ikeja Electric Band A feeder only got 6 hours yesterday. We pay ₦206/kWh. Meter: 45019284721",
        "media_type": "text"
    }
    res_chat = client.post("/api/simulate-chat", json=payload)
    assert res_chat.status_code == 200
    chat_data = res_chat.json()
    print("  ✓ PowerWatch Bot Reply Received:")
    print("  " + "\n  ".join(chat_data["reply"].split("\n")[:8]) + "\n  ...")
    assert "PowerWatch" in chat_data["reply"] or "CheckLocal" in chat_data["reply"]
    assert "Meter Corroborated" in chat_data["reply"] or "45019284721" in chat_data["reply"] or "45019" in chat_data["reply"]
    assert "Phase 2" in chat_data["reply"]
    assert chat_data["points_earned"] > 0
    print(f"  ✓ Points Awarded: +{chat_data['points_earned']} pts | Badge: {chat_data['user_badge']}")

    # 6. Web Report Submission
    print("\n[6] Testing POST /api/reports/submit...")
    report_payload = {
        "user_id": "citizen_tester",
        "country": "Nigeria",
        "location": "Gwarinpa Estate, Abuja",
        "category": "power_status",
        "content": "AEDC feeder on 3rd Avenue is billing Band A rate of ₦209.50 but light only stayed 4 hours. Meter: 01283948572",
        "source": "web"
    }
    res_rep = client.post("/api/reports/submit", json=report_payload)
    assert res_rep.status_code == 200
    rep_data = res_rep.json()
    print(f"  ✓ Report Verified! Category: {rep_data['category']} | Confidence: {rep_data['confidence_level']}")
    print(f"  ✓ Next Action: {rep_data['next_action']}")

    # 7. Twilio WhatsApp Webhook
    print("\n[7] Testing POST /api/webhook/twilio (TwiML Response)...")
    webhook_form = {
        "From": "whatsapp:+2348099887766",
        "Body": "AEDC Gwarinpa light out since 2pm, meter 01283948572"
    }
    res_tw = client.post("/api/webhook/twilio", data=webhook_form)
    assert res_tw.status_code == 200
    assert "application/xml" in res_tw.headers.get("content-type", "")
    assert "<Response>" in res_tw.text
    assert "<Message>" in res_tw.text
    print("  ✓ Valid TwiML XML returned successfully for Twilio WhatsApp!")

    # 8. Frontend Static Mounting
    print("\n[8] Testing GET / (PowerWatch Landing Mirror)...")
    res_ui = client.get("/")
    assert res_ui.status_code == 200
    assert "PowerWatch" in res_ui.text
    assert "CheckLocal" in res_ui.text
    assert "WhatsApp Simulator" in res_ui.text
    assert "docketModal" in res_ui.text
    print("  ✓ Public web mirror loaded successfully with PowerWatch branding!")

    print("\n" + "=" * 60)
    print("🎉 ALL 8 POWERWATCH END-TO-END TESTS PASSED WITH 100% SUCCESS!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
