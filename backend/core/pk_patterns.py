# backend/core/pk_patterns.py

from presidio_analyzer import Pattern, PatternRecognizer

# CNIC: 5 digits - 7 digits - 1 digit  (e.g. 35202-1234567-1)
CNIC_REGEX = r"\d{5}-\d{7}-\d{1}"

# PK Mobile: covers 03001234567, 0300-1234567, +923001234567
PK_MOBILE_REGEX = r"(\+92|0)3\d{2}-?\d{7}"

# PK Landline: 2-4 digit city code - 6-8 digit number (e.g. 042-35761234)
PK_LANDLINE_REGEX = r"0(?!3)\d{1,3}-\d{6,8}"


def get_pk_recognizers():
    """
    Builds Presidio PatternRecognizers for Pakistani PII types
    (CNIC, mobile, landline) that Presidio doesn't know out of the box.
    """
    cnic_recognizer = PatternRecognizer(
        supported_entity="PK_CNIC",
        patterns=[Pattern(name="cnic_pattern", regex=CNIC_REGEX, score=0.85)],
        context=["cnic", "id card", "identity", "national id"],
    )

    mobile_recognizer = PatternRecognizer(
        supported_entity="PK_MOBILE",
        patterns=[Pattern(name="mobile_pattern", regex=PK_MOBILE_REGEX, score=0.8)],
        context=["phone", "mobile", "contact", "cell", "whatsapp"],
    )

    landline_recognizer = PatternRecognizer(
        supported_entity="PK_LANDLINE",
        patterns=[Pattern(name="landline_pattern", regex=PK_LANDLINE_REGEX, score=0.7)],
        context=["phone", "landline", "office", "contact"],
    )

    return [cnic_recognizer, mobile_recognizer, landline_recognizer]