# backend/core/detector.py

from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from core.pk_patterns import get_pk_recognizers
from config.settings import SPACY_MODEL


def build_analyzer():
    """
    Builds and returns a Presidio AnalyzerEngine configured with:
    - spaCy (en_core_web_sm) as the underlying NLP engine
    - Default Presidio recognizers (email, credit card, generic names, etc.)
    - Our custom Pakistani recognizers (CNIC, mobile, landline)
    """
    # Tell Presidio which spaCy model to use
    nlp_config = {
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": "en", "model_name": SPACY_MODEL}],
    }
    nlp_engine = NlpEngineProvider(nlp_configuration=nlp_config).create_engine()

    # Create the analyzer with that engine
    analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["en"])

    # Register our custom PK recognizers on top of the built-in ones
    for recognizer in get_pk_recognizers():
        analyzer.registry.add_recognizer(recognizer)

    return analyzer


# Build once at import time so we don't reload spaCy on every request
analyzer_engine = build_analyzer()


def detect_pii(text: str):
    """
    Runs PII detection on input text.
    Returns a list of Presidio RecognizerResult objects — each has:
    entity_type, start, end, score
    """
    results = analyzer_engine.analyze(text=text, language="en")
    return results

from presidio_analyzer import RecognizerResult
from core.llm_fallback import detect_pii_llm


def detect_pii_combined(text: str):
    """
    Runs both detection layers and merges results:
    1. Presidio (regex + spaCy) - structured, pattern-based
    2. Groq LLM fallback - catches context-dependent PII Presidio misses

    Returns a single combined list, same format for both sources.
    """
    presidio_results = detect_pii(text)

    llm_findings = detect_pii_llm(text)
    llm_results = []

    for finding in llm_findings:
        found_text = finding.get("text", "")
        entity_type = finding.get("entity_type", "OTHER")

        # Find where this text actually appears in the original string
        start_index = text.find(found_text)

        # Skip if the LLM hallucinated text that isn't actually in the input
        if start_index == -1:
            continue

        end_index = start_index + len(found_text)

        llm_results.append(
            RecognizerResult(
                entity_type=f"LLM_{entity_type}",
                start=start_index,
                end=end_index,
                score=0.75,  # fixed confidence for LLM-sourced findings
            )
        )

    return presidio_results + llm_results