# Sentinel-PII

An AI-powered PII (Personally Identifiable Information) detection and anonymization engine — built for Pakistani data formats, deployed as a full-stack app.

Sentinel-PII scans text and automatically detects and redacts sensitive personal information — names, Pakistani CNIC numbers, mobile and landline numbers, emails — before that text is stored, shared, or used elsewhere (e.g. training a chatbot, logging support tickets).

## 🔗 Live Demo

- **Frontend:** [https://sentinel-pii.vercel.app]
- **Backend API:** [https://py-saqlain-sentinel-pii-backend.hf.space](https://py-saqlain-sentinel-pii-backend.hf.space)



## How it works

Sentinel-PII combines three detection layers:

1. **Presidio (Microsoft's open-source PII detection engine)** + **spaCy** — detects structured entities like emails and names using NLP.
2. **Custom regex recognizers** — built specifically for Pakistani formats (CNIC, mobile, landline numbers) that Presidio doesn't support out of the box.
3. **Groq LLM fallback** — catches context-dependent PII that pattern-matching misses (e.g. nicknames, informally mentioned personal details), using a fast open-source LLM.

Each detection is scored for confidence. Low-confidence noise is filtered out before anonymization, and the anonymization layer supports three strategies: **mask**, **replace with label**, or **hash**.

## Tech Stack

**Backend:** Python, FastAPI, Presidio, spaCy, Groq API, Pydantic, pytest
**Frontend:** React (Vite), Axios
**Deployment:** Hugging Face Spaces (backend), Vercel (frontend)

## Architecture

```
React Frontend (Vercel)
        │
        │ HTTPS POST /anonymize
        ▼
FastAPI Backend (Hugging Face Spaces)
        │
        ├── Presidio + spaCy  →  NLP-based detection
        ├── Custom regex      →  Pakistani CNIC/phone patterns
        └── Groq LLM fallback →  context-aware detection
        │
        ▼
Anonymized text (mask / replace / hash)
```

## Running locally

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Add a `.env` file in `backend/` with:
```
GROQ_API_KEY=your_key_here
```

## Testing

```bash
cd backend
pytest tests/test_pk_patterns.py -v
```

## Notes

- Deployed on Hugging Face's free ZeroGPU tier — the API itself is CPU-only; the ZeroGPU requirement is satisfied via a lightweight startup check with no actual GPU workload.
- Built as a portfolio project to demonstrate a hybrid detection architecture (regex + NLP + LLM) beyond a single-technique PII tool.
