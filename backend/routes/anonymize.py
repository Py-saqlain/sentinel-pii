# backend/routes/anonymize.py

from fastapi import APIRouter
from models.schemas import AnonymizeRequest, AnonymizeResponse
from core.detector import detect_pii
from core.anonymizer import anonymize_text, SCORE_THRESHOLD
from core.detector import detect_pii_combined

router = APIRouter()


@router.post("/anonymize", response_model=AnonymizeResponse)
def anonymize(request: AnonymizeRequest):
    # Step 1: find PII in the text
    results = detect_pii_combined(request.text)

    # Step 2: count only the ones that pass our confidence threshold
    entities_found = len([r for r in results if r.score >= SCORE_THRESHOLD])

    # Step 3: redact the text using the chosen strategy
    anonymized = anonymize_text(request.text, results, strategy=request.strategy)

    return AnonymizeResponse(
        original_text=request.text,
        anonymized_text=anonymized,
        entities_found=entities_found,
    )