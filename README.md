# Sharks

AI-first student engagement ecosystem for Indian students planning higher studies.

## Product thesis

The core USP is a WhatsApp-first experience that behaves like a student companion for discovery, guidance, and loan conversion. The prototype is built to feel like a voice-friendly, low-friction, always-available assistant. The first working build focuses on WhatsApp; OCR is intentionally kept optional for later.

## What is implemented

- WhatsApp webhook verification and message handling
- AI mentor endpoint with Gemini fallback logic
- Country/course recommendation engine
- Admission probability scoring
- ROI and salary estimation engine
- Loan eligibility and simulated offers
- Document parsing stub for the future OCR phase
- SQLite-backed demo storage for profiles, messages, and documents

## Problem statement fit

This prototype covers the student journey end to end:

1. Discovery of countries, universities, and courses
2. AI-guided doubt solving through chat
3. Admission likelihood estimation
4. ROI and salary planning
5. Loan eligibility and offer discovery
6. Document collection and auto-fill support

## Final stack decision

- WhatsApp provider: Meta WhatsApp Cloud API
- LLM provider: Google Gemini API
- Database: SQLite for demo, PostgreSQL later for hosted deployment
- OCR: optional later, Google Vision or AWS Textract

## Project structure

- [main.py](main.py) — thin entrypoint
- [sharks/app.py](sharks/app.py) — FastAPI app factory and router wiring
- [sharks/config.py](sharks/config.py) — environment settings
- [sharks/db.py](sharks/db.py) — database connection and schema creation
- [sharks/schemas.py](sharks/schemas.py) — request models and domain dataclass
- [sharks/repository.py](sharks/repository.py) — persistence helpers
- [sharks/services/whatsapp.py](sharks/services/whatsapp.py) — WhatsApp workflow and webhook parsing
- [sharks/services/llm.py](sharks/services/llm.py) — Gemini integration and fallback mentor logic
- [sharks/services/recommendations.py](sharks/services/recommendations.py) — career navigator logic
- [sharks/services/admissions.py](sharks/services/admissions.py) — admission scoring logic
- [sharks/services/roi.py](sharks/services/roi.py) — ROI calculator
- [sharks/services/loans.py](sharks/services/loans.py) — loan eligibility engine
- [sharks/services/documents.py](sharks/services/documents.py) — document parsing stub
- [sharks/api/routes.py](sharks/api/routes.py) — core REST APIs
- [sharks/api/whatsapp.py](sharks/api/whatsapp.py) — WhatsApp webhook and send API

## Environment variables

Edit [.env](.env) and fill these later:

- `WHATSAPP_API_TOKEN`
- `WHATSAPP_PHONE_NUMBER_ID`
- `WHATSAPP_VERIFY_TOKEN`
- `WHATSAPP_APP_SECRET`
- `LLM_API_KEY`
- `LLM_MODEL`
- `OCR_API_KEY`
- `OCR_API_URL`
- `DATABASE_URL`
- `APP_BASE_URL`

Current local demo values:

- `DATABASE_URL=sqlite:///./sharks.db`
- `APP_BASE_URL=http://127.0.0.1:8000`

## How to run

1. Install dependencies:

```bash
uv sync
```

2. Start the app:

```bash
uv run python main.py
```

3. Open the health check:

- [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

## How to test quickly

### 1. Root check

Open the base URL:

- [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### 2. Profile API

Send a profile payload to [POST /api/profile](http://127.0.0.1:8000/docs) using Swagger UI or a REST client.

### 3. Mentor API

Use [POST /api/mentor](http://127.0.0.1:8000/docs) with a WhatsApp ID and message.

### 4. Recommendation and scoring APIs

Test these endpoints from Swagger UI:

- [POST /api/recommend](http://127.0.0.1:8000/docs)
- [POST /api/admission-score](http://127.0.0.1:8000/docs)
- [POST /api/roi](http://127.0.0.1:8000/docs)
- [POST /api/loan-eligibility](http://127.0.0.1:8000/docs)

### 5. WhatsApp webhook

- Verification endpoint: [GET /webhook/whatsapp](http://127.0.0.1:8000/webhook/whatsapp)
- Inbound message endpoint: [POST /webhook/whatsapp](http://127.0.0.1:8000/webhook/whatsapp)
- Send message endpoint: [POST /api/whatsapp/send](http://127.0.0.1:8000/docs)

## API flow summary

1. User sends a WhatsApp message.
2. Webhook extracts sender and text.
3. System stores the event.
4. Routing logic decides whether to answer with mentor, recommendation, loan, or ROI output.
5. Reply is sent back over WhatsApp.
6. Profile and document data are stored locally.

## OCR note

OCR is intentionally optional for now. The document module currently parses raw text in demo mode and can be connected to Google Vision or AWS Textract later.

## Build order used

1. Modularized the backend into separate files
2. Wired the FastAPI app factory
3. Moved WhatsApp handling into its own service and router
4. Split recommendation, admission, ROI, loan, and document logic into services
5. Kept the database simple with SQLite for the demo
6. Added run and test instructions here in the README

## Notes for the demo

- The WhatsApp experience is the primary differentiator.
- The backend is modular and easy to extend.
- The system is ready for real keys when you add them.

## Next step

Add your API keys to [.env](.env), start the app, and test each endpoint in Swagger UI or with WhatsApp Cloud API webhooks.
