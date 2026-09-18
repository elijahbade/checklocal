# AI Methodology & Responsible Civic Implementation

> **OSF × Andela Hackathon 2026 — Track: Transparency & Accountability / Social Cohesion**  
> **Project: CheckLocal**

This document details the architectural decisions, safety guardrails, prompt engineering, and ethical AI practices implemented in CheckLocal to maximize transparency, accessibility, and trust.

---

## 1. Why AI? The Civic Information Bottleneck

In African contexts (Nigeria, Kenya, South Africa), the information gap is not a lack of data; it is **unstructured, fragmented, and viral communication**.
- Citizens exchange unstructured voice notes, text messages, and screenshots inside private WhatsApp groups.
- Official regulatory agencies (e.g. NMDPRA, NERC, EPRA, Eskom) publish updates via PDF circulars, technical press releases, or obscure websites that ordinary citizens cannot easily parse or access under data constraints.
- Existing general-purpose chatbots hallucinate, speak in academic English, and lack local market context.

CheckLocal utilizes **Google Gemini 3.7 Flash** (via the official `google-genai` SDK) not as a generic conversational bot, but as a **constrained, multi-task civic processing pipeline**.

---

## 2. Multi-Task AI Processing Pipeline

Every incoming report (text, transcribed voice note, or forwarded claim) undergoes five deterministic stages:

```
[ Incoming Citizen Message ]
             │
             ▼
[ 1. Entity & Category Extraction ] ──► (Fuel, Food Staple, Power, Water, Rumor)
             │
             ▼
[ 2. Truth Triangulation & Grounding ] ──► (Cross-reference with community consensus & regulatory benchmarks)
             │
             ▼
[ 3. Confidence & Risk Scoring ] ──► (Verified >90%, High >80%, Community Consensus, Unverified)
             │
             ▼
[ 4. Dual Cultural Translation ] ──► (Plain English + Authentic Nigerian Pidgin English)
             │
             ▼
[ 5. Actionable Civic Prescription ] ──► (Single verifiable next step: hotline, boycott, or debunk broadcast)
```

---

## 3. Mitigating Hallucination & Ensuring Accuracy

Civic trust is fragile. A single hallucinated fuel price can cause real financial harm. CheckLocal implements strict anti-hallucination protocols:

1. **System Prompt Constraint**: The Gemini model is instructed to output strictly structured JSON conforming to explicit schema keys (`category`, `confidence_level`, `confidence_score`, `verified_summary_en`, `verified_summary_pidgin`, `sources`, `next_action`).
2. **Benchmark Grounding**: Verification summaries must cite the specific sources of verification (e.g. *“42 verified citizen reports + NMDPRA Retail Tracker”*).
3. **Refusal to Validate Unsubstantiated Claims**: If a claim has zero corroborating evidence, the AI categorizes it as `investigating` or explicitly marks it as `UNVERIFIED / VIRAL CLAIM`, warning users not to forward it.
4. **Deterministic Heuristic Fallback**: In low-connectivity environments or when API rate limits occur, CheckLocal activates a localized heuristic rule engine with pre-verified regional price bands and official hotlines, ensuring zero downtime.

---

## 4. Linguistic Accessibility: Bridging the Digital Divide with Nigerian Pidgin

Most AI tools speak only formal Queen's English, immediately alienating millions of market women, transport operators (Danfo/Matatu drivers), and grassroots citizens.

- CheckLocal prompts Gemini to generate a parallel translation in **natural, everyday Nigerian Pidgin English**.
- For example:
  - *Plain English*: "Petrol is selling between ₦850 and ₦890 per litre across major stations. No acute scarcity observed."
  - *Nigerian Pidgin*: "Fuel dey sell around ₦850 to ₦890 for major stations like NNPC and Total. Normal dispensing dey go on, no need to panic buy."
- This drastically improves comprehension, emotional connection, and trust among everyday citizens.

---

## 5. Right Use of AI: Development Process Disclosure

In compliance with hackathon transparency guidelines, AI was utilized throughout the software development lifecycle:
- **Pair Programming & Architecture**: Google DeepMind's Antigravity agent was utilized for system planning, database schema modeling, and async FastAPI route scaffolding.
- **Test-Driven AI Validation**: Automated test suites were written to systematically evaluate model outputs against edge cases (e.g., sudden subsidy rumors, fake power outage circulars).
- **Rapid UI/UX Implementation**: A bespoke, accessible Vanilla CSS design system with mobile-first responsiveness and an in-browser WhatsApp simulator was crafted and optimized.

---

## 6. Alignment with Hackathon Tracks

| Track | CheckLocal AI Contribution |
| :--- | :--- |
| **Transparency & Accountability** | Makes opaque retail prices (fuel, food) and utility service blackouts transparent, holding station operators and Discos accountable. |
| **Stability & Social Cohesion** | Debunks panic-inducing WhatsApp viral rumors in under 15 seconds, preventing unnecessary bank runs, panic buying, and civil unrest. |
