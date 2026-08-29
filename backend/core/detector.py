# backend/core/detector.py

from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from core.pk_patterns import get_pk_recognizers


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
        "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}],
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