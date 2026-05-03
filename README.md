# Sharks

AI-first student engagement ecosystem for Indian students planning higher studies.

## Product thesis

The core USP is a WhatsApp-first experience that acts like a student companion for discovery, guidance, and loan conversion. The public-facing story is a voice-enabled, low-friction, always-available assistant for students with minimal internet dependency. The first working prototype will focus on the WhatsApp journey; the rest of the ecosystem will be simulated or added incrementally.

## Problem statement fit

This prototype addresses the end-to-end student journey:

1. Discovery of countries, universities, and courses
2. AI-guided doubt solving through chat
3. Admission likelihood estimation
4. ROI and salary planning
5. Loan eligibility and offer discovery
6. Document collection and auto-fill support

## MVP scope for this build

### Phase 1: WhatsApp-first engagement layer
- Student onboarding through WhatsApp
- Conversational mentor for queries
- Career navigator based on profile inputs
- Admission probability scoring
- ROI and salary estimation
- Loan eligibility check with simulated offers

### Phase 2: Conversion and automation layer
- Document upload over WhatsApp
- OCR-based extraction of key fields
- Auto-fill for loan forms
- Smart nudges and follow-ups

### Phase 3: Growth and retention layer
- Personalized journeys
- Content recommendations
- Referral and engagement loops
- Automated reminders for deadlines and next steps

## Proposed user flow

1. User discovers the assistant on WhatsApp
2. Bot collects profile details in a guided format
3. AI returns country/course recommendations
4. Bot estimates admission probability and ROI
5. Bot checks indicative loan eligibility
6. User uploads documents on WhatsApp
7. System extracts data and prepares the loan flow

## Core modules

### 1. AI Conversational Mentor
Handles student queries about course selection, visa doubts, applications, timelines, and loans.

### 2. AI Career Navigator
Suggests countries, universities, and courses based on marks, budget, work experience, and preferences.

### 3. Admission Probability Predictor
Uses rule-based scoring or lightweight heuristics to estimate admission chance.

### 4. ROI and Salary Prediction Engine
Calculates expected salary, cost of education, and payback period using benchmark salary data and formulas.

### 5. Loan Eligibility and Offer Engine
Evaluates loan eligibility from academic and financial inputs and shows demo offers aligned with NBFC-style products.

### 6. Document Processing and Auto-Fill
Extracts data from PAN, admit letter, and income proof uploaded over WhatsApp using OCR.

## AI / API stack needed

### Required for the prototype
- WhatsApp Cloud API
- Google Gemini API for LLM/chat
- PostgreSQL database via Neon or Supabase

### Optional for later phases
- Auth backend
- Vector search for memory and knowledge retrieval
- Analytics and notification APIs

## Final stack decision

### 1. WhatsApp provider
Use Meta WhatsApp Cloud API.

Why:
- Official API
- Easy webhook flow
- Good fit for the WhatsApp-first USP

### 2. LLM provider
Use Google Gemini API, starting with Gemini Flash models.

Why:
- Fast
- Low-cost / free-tier friendly
- Good enough for chatbot, summarization, and content generation

### 3. Database
Use PostgreSQL.

Recommended connection style:
- Local dev: `sqlite:///./sharks.db` if needed for quick testing
- Hosted dev/prod: `postgresql+psycopg://USER:PASSWORD@HOST:PORT/DBNAME`

Recommended provider:
- Neon or Supabase Postgres

### 4. OCR
Keep OCR optional for the end.

Suggested later provider:
- Google Vision OCR or AWS Textract

## How to generate the required API keys

### WhatsApp Cloud API
1. Create a Meta Developer app.
2. Add the WhatsApp product.
3. Connect a test phone number.
4. Copy the phone number ID.
5. Generate a permanent access token.
6. Set a webhook verify token of your choice.

### Google Gemini API
1. Open Google AI Studio.
2. Create a new API key.
3. Save it as `LLM_API_KEY`.
4. Set `LLM_MODEL` to a Flash model name.

### PostgreSQL database
1. Create a Neon or Supabase project.
2. Create a Postgres database.
3. Copy the connection string.
4. Store it in `DATABASE_URL`.

### OCR later
1. Choose Google Vision or AWS Textract.
2. Create credentials only when the document flow is added.
3. Keep the OCR env vars empty until then.

## APIs to implement next

1. WhatsApp inbound webhook handler
2. WhatsApp outbound message sender
3. User profile capture endpoint
4. Recommendation engine endpoint
5. Admission score endpoint
6. ROI calculator endpoint
7. Loan eligibility endpoint
8. Document upload and OCR endpoint
9. Auto-fill payload generator endpoint
10. Conversation state / session storage endpoint

## Environment variables needed

Create a local `.env` file with these keys:

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

## Build order

1. Set up WhatsApp integration skeleton
2. Add message routing and session state
3. Implement profile intake flow
4. Add recommendation and scoring logic
5. Add ROI and loan eligibility calculators
6. Add document upload and OCR stubs
7. Wire the outputs into a polished demo flow

## Notes for the demo

- The prototype can simulate backend logic where needed.
- The WhatsApp experience is the main differentiator.
- The system should feel like a complete student companion, not just a chatbot.

## Next step

Implement the WhatsApp API flow first, then layer in the mentor, recommendation, scoring, and loan modules one by one.
