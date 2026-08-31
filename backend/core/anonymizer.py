# backend/core/anonymizer.py

from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

anonymizer_engine = AnonymizerEngine()

# Minimum confidence score required to keep a detection.
# Anything below this is treated as noise and ignored.
SCORE_THRESHOLD = 0.4


def anonymize_text(text: str, analyzer_results: list, strategy: str = "mask"):
    """
    Takes original text + Presidio's detection results, and returns
    the text with PII redacted according to the chosen strategy.

    strategy options:
      - "mask"     -> replaces PII with asterisks, e.g. ***********
      - "replace"  -> replaces PII with a label, e.g. <PK_CNIC>
      - "hash"     -> replaces PII with a hash of itself (consistent per value)
    """
    # Step 1: filter out low-confidence noise
    filtered_results = [r for r in analyzer_results if r.score >= SCORE_THRESHOLD]

    # Step 2: define how each strategy should behave
    if strategy == "mask":
        operators = {
            "DEFAULT": OperatorConfig("mask", {
                "masking_char": "*",
                "chars_to_mask": 100,
                "from_end": False,
            })
        }
    elif strategy == "replace":
        operators = {
            "DEFAULT": OperatorConfig("replace", {"new_value": "<REDACTED>"})
        }
    elif strategy == "hash":
        operators = {
            "DEFAULT": OperatorConfig("hash", {"hash_type": "sha256"})
        }
    else:
        raise ValueError(f"Unknown strategy: {strategy}")

    # Step 3: anonymizer handles overlap resolution internally,
    # then applies the chosen operator to each remaining match
    result = anonymizer_engine.anonymize(
        text=text,
        analyzer_results=filtered_results,
        operators=operators,
    )

    return result.text