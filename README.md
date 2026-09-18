# CheckLocal (WhatsApp-First Civic Fact-Checking Platform)

[![Hackathon: OSF x Andela](https://img.shields.io/badge/Hackathon-OSF%20%C3%97%20Andela%202026-059669.svg)](https://andela.com)
[![Track: Transparency & Accountability](https://img.shields.io/badge/Track-Transparency%20%26%20Accountability-047857.svg)](#)
[![Track: Stability & Social Cohesion](https://img.shields.io/badge/Track-Stability%20%26%20Social%20Cohesion-065F46.svg)](#)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com)
[![Google Gemini AI](https://img.shields.io/badge/AI-Google%20Gemini%203.7%20Flash-4285F4.svg)](https://ai.google.dev)
[![AI Methodology](https://img.shields.io/badge/Methodology-Responsible%20AI%20Architecture-purple.svg)](AI_METHODOLOGY.md)

> **"Information you can trust — where people actually live and talk: on WhatsApp."**
> 
> 📄 **Reviewers & Judges**: Please see [AI_METHODOLOGY.md](AI_METHODOLOGY.md) for our detailed breakdown on responsible AI architecture, anti-hallucination guardrails, and Nigerian Pidgin localization.

---

## 🌍 Hackathon Context & Core Problem

- **Hackathon**: OSF × Andela Hackathon – *“Information you can trust”* (Deadline: 21 September 2026)
- **Primary Track**: Transparency & Accountability
- **Secondary Track**: Stability & Social Cohesion
- **Focus Countries**: **Nigeria** (primary), **Kenya**, **South Africa**

### The Daily Reality
Ordinary people in Lagos, Nairobi, and Johannesburg get the vast majority of their daily civic and cost-of-living information—fuel prices, food commodity rates, power blackouts, and water cuts—via **family and neighborhood WhatsApp groups**. 

During price shocks or grid collapses:
1. **Unverified rumors spread virally** (e.g., false claims of sudden fuel price drops, fake strike declarations, manufactured shortages).
2. **Official regulatory websites are slow, hard to reach, or low in public trust**.
3. **Panic-buying ensues**, causing social anxiety, hoarding, and extortion by unscrupulous middlemen.

### The CheckLocal Solution
**CheckLocal** is a **WhatsApp-first civic verification engine + public web mirror**.
Citizens simply forward a message, voice note, receipt, or text claim directly to CheckLocal on WhatsApp. In **under 15 seconds**, CheckLocal replies in **Plain English and Nigerian Pidgin** with:
1. **A verified factual summary**
2. **Confidence rating + cross-referenced sources** (community reports + regulatory benchmarks)
3. **One clear next action** (e.g., reporting price gouging to consumer watchdogs or sharing a debunk notice with street associations)
4. **Civic Trust Points** to incentivize constructive reporting
5. **A public web trending mirror** so anyone without WhatsApp can search and view verified community facts in real time.

---

## 🚀 Key Features

### 1. WhatsApp Bot (Primary Civic Interface)
- **Multi-format ingestion**: Handles plain text reports, forwarded messages, voice note transcripts, and screenshot receipts.
- **5 Core Report Categories**:
  - ⛽ **Local Fuel/Petrol Price**: PMS, diesel, pump rate benchmarks, retail station queue status.
  - 🌾 **Food Staple Prices**: Garri, rice, maize meal (Unga), cooking oil, bread across regional markets (e.g., Mile 12, Bodija, Wuse).
  - ⚡ **Power / Electricity Status**: Feeder outages, Disco maintenance (EKEDC, IKEDC, AEDC), Kenya Power (KPLC), and Eskom load shedding.
  - 💧 **Water Utility Status**: Municipal pipe bursts, borehole supplies, Rand Water reservoir recovery.
  - 🔍 **Circulating Rumors & Claims**: Debunking viral audio clips, false price announcements, and strike notices.
- **Dual-Language Replies**: Every response is generated in both **Plain English** and authentic **Nigerian Pidgin English** to ensure maximum accessibility across literacy and educational backgrounds.
- **Light Gamification / Civic Trust Points**: Earn points (`+10 pts` to `+15 pts`) and civic badges (*Civic Scout*, *Local Watchdog*, *Trust Champion*).
- **Roadmap Suffix**: Every bot message ends with: `Coming soon: Local Ambassador programme + other civic tools.`

### 2. Public Web Mirror & Interactive Simulator
- **Trending Local Facts Feed**: Real-time cards filterable by country (Nigeria, Kenya, South Africa) and category, with a search bar and language switcher.
- **Interactive WhatsApp Bot Simulator**: A live smartphone simulator embedded directly on the web page. Judges and users can test the full conversational WhatsApp bot experience instantly in their browser without requiring a live paid Twilio/Meta number!
- **Web Report Submission**: A clean form for citizens to submit reports from the web with an instant AI verification preview.
- **Official Regulatory Benchmarks**: Direct access to verified benchmarks from NMDPRA, NERC, FCCPC, EPRA, and DMRE.

### 3. Production Webhook Support
- `POST /api/webhook/twilio`: Ingests real WhatsApp messages via Twilio API and returns standard TwiML XML.
- `POST /api/webhook/meta` & `GET /api/webhook/meta`: Webhook verification and event handler for Meta WhatsApp Cloud API.

---

## 🏗️ System Architecture

```
                               ┌──────────────────────────────────────────┐
                               │              Everyday Citizen            │
                               └────────────────────┬─────────────────────┘
                                                    │
                      ┌─────────────────────────────┴────────────────────────────┐
                      ▼                                                          ▼
        [ WhatsApp / Twilio / Meta ]                                [ Public Web Mirror ]
                      │                                             (Trending Feed & Simulator)
                      ▼                                                          │
          /api/webhook/twilio or /meta                                           ▼
                      │                                               /api/reports, /api/trending
                      └─────────────────────────────┬────────────────────────────┘
                                                    ▼
                                     ┌─────────────────────────────┐
                                     │    FastAPI Backend Engine   │
                                     │  - Report Parser & Router   │
                                     │  - Civic Points Calculator  │
                                     └──────────────┬──────────────┘
                                                    │
                       ┌────────────────────────────┴────────────────────────────┐
                       ▼                                                         ▼
         ┌─────────────────────────────┐                           ┌───────────────────────────┐
         │       Gemini AI Engine      │                           │      SQLite Database      │
         │ - Categorization & Entity   │                           │ - Reports & Submissions   │
         │ - Confidence & Benchmark    │                           │ - Trending Fact Clusters  │
         │ - English + Pidgin Summary  │                           │ - Civic Trust Points Log  │
         │ - Action Recommendation     │                           │ - Benchmark Price Feeds   │
         └─────────────────────────────┘                           └───────────────────────────┘
```

---

## 🤖 How AI Coding Tools Were Used in This Project

In accordance with hackathon guidelines, this project demonstrates the powerful, ethical, and practical use of modern AI tools to accelerate social-impact civic engineering:

1. **AI Architectural Orchestration**: Designed with Google DeepMind's **Antigravity AI Agent**, following systematic planning workflows, requirement decomposition, and test-driven verification.
2. **LLM Verification Pipeline**: Uses the official `google-genai` SDK with **Gemini 3.7 Flash** for multimodal message classification, semantic fact cross-referencing, confidence scoring, and generation of culturally authentic Nigerian Pidgin translations.
3. **Resilient Fallback Design**: AI heuristic modeling was used to build an offline rule-based knowledge engine containing regional market benchmarks so the application functions seamlessly even in low-bandwidth or offline environments.
4. **Code Generation & Quality**: FastAPI asynchronous route architecture, SQLAlchemy ORM data models, and a bespoke vanilla CSS design system were rapidly crafted, linted, and verified using automated test harnesses.

---

## 🛠️ Quick Start & Local Setup

### Prerequisites
- Python 3.10+ (Tested on Python 3.10 – 3.14)
- (Optional) Free Google Gemini API Key from [Google AI Studio](https://aistudio.google.com)

### 1. Clone & Navigate to Project
```bash
git clone https://github.com/your-repo/checklocal.git
cd checklocal
```

### 2. Set Up Virtual Environment & Install Dependencies
```bash
# Create virtual environment
python -m venv .venv

# Activate environment
# On Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# On macOS / Linux:
source .venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

### 3. Configure Environment Variables (Optional)
Copy `.env.example` to `.env`:
```bash
cp backend/.env.example backend/.env
```
*(If `GEMINI_API_KEY` is not set, CheckLocal automatically runs in intelligent civic heuristic mode with pre-seeded ground truth, making judging instant and error-free!)*

### 4. Run CheckLocal
```bash
python run_server.py
```

### 5. Access the Platform
- **Public Web Mirror & WhatsApp Simulator**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Twilio Webhook Endpoint**: `http://127.0.0.1:8000/api/webhook/twilio`
- **Meta Cloud API Webhook**: `http://127.0.0.1:8000/api/webhook/meta`

---

## 📲 Testing the WhatsApp Bot

### Option A: Immediate In-Browser Simulator (No Setup Needed!)
1. Open [http://127.0.0.1:8000](http://127.0.0.1:8000).
2. On the right side of the screen, see the **CheckLocal Bot Smartphone Simulator**.
3. Click any of the quick-prompt chips:
   - `⛽ Fuel in Ikeja?`
   - `🌾 Garri at Mile 12?`
   - `⚡ Power in Lekki?`
   - `🔍 Petrol dropping to ₦450?`
   - `🇰🇪 Nairobi Unga?`
   - `🇿🇦 Eskom status?`
4. Watch the simulated typing dots and receive the verified, dual-language response with earned points and next actions in seconds!

### Option B: Connecting a Real WhatsApp Number via Twilio
1. Start an ngrok tunnel to your local server:
   ```bash
   ngrok http 8000
   ```
2. In your Twilio Console (WhatsApp Sandbox):
   - Set **"WHEN A MESSAGE COMES IN"** to:  
     `https://your-ngrok-url.ngrok-free.app/api/webhook/twilio` (HTTP POST).
3. Send any message from your physical phone's WhatsApp to your Twilio WhatsApp number.

---

## 🗺️ Roadmap & Phase 2 Vision: Local Ambassador Programme

Marked as *"Coming Soon"* for the hackathon MVP:
- **Grassroots Sentinel Network**: Partnering with market associations, transport unions (NURTW), and community leaders to conduct physical meter spot-checks.
- **Civic Trust Token / Airtime Vouchers**: Enabling active reporters to redeem verified civic trust points for mobile talk time and data bundles.
- **Verified Merchant Badges**: Providing physical QR stickers for market vendors selling at fair regulatory benchmark prices.
- **Expanded Indigenous Languages**: Expanding translations beyond Nigerian Pidgin to include **Yoruba, Hausa, Igbo, Swahili, and isiZulu**.

---

## ⚖️ License
Open-source under the [MIT License](LICENSE). Built with pride for the **OSF × Andela Hackathon 2026**.
