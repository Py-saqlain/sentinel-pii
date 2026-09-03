# backend/tests/test_pk_patterns.py

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import re
from core.pk_patterns import CNIC_REGEX, PK_MOBILE_REGEX, PK_LANDLINE_REGEX


def test_cnic_valid_format_matches():
    assert re.search(CNIC_REGEX, "35202-1234567-1")


def test_cnic_missing_dash_does_not_match():
    assert not re.fullmatch(CNIC_REGEX, "352021234567 1")


def test_mobile_matches_with_dash():
    assert re.search(PK_MOBILE_REGEX, "0300-1234567")


def test_mobile_matches_without_dash():
    assert re.search(PK_MOBILE_REGEX, "03001234567")


def test_mobile_matches_international_format():
    assert re.search(PK_MOBILE_REGEX, "+923001234567")


def test_landline_matches():
    assert re.search(PK_LANDLINE_REGEX, "042-35761234")


def test_landline_does_not_match_mobile_number():
    # This confirms the (?!3) fix we made earlier actually works
    match = re.fullmatch(PK_LANDLINE_REGEX, "0300-1234567")
    assert match is None