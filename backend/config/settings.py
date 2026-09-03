# backend/config/settings.py

import os
from dotenv import load_dotenv

load_dotenv()

# --- Detection settings ---
SCORE_THRESHOLD = 0.4          # minimum confidence to keep a detection
LLM_CONFIDENCE_SCORE = 0.75    # fixed score assigned to LLM-sourced findings

# --- Groq settings ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "openai/gpt-oss-120b"

# --- spaCy settings ---
SPACY_MODEL = "en_core_web_sm"

# --- CORS settings ---
# For local development only. Restrict this to your actual frontend
# domain before deploying to production.
CORS_ALLOWED_ORIGINS = ["*"]