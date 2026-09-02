# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.anonymize import router as anonymize_router

app = FastAPI(title="Sentinel-PII API")

# Allow the React frontend (running on a different port) to call this API.
# Without this, the browser blocks the request for security reasons.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for local dev only — we'll restrict this later for production
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(anonymize_router)


@app.get("/")
def root():
    return {"status": "Sentinel-PII API is running"}