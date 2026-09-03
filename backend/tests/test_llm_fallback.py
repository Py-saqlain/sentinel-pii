# backend/tests/test_llm_fallback.py

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.llm_fallback import detect_pii_llm

sample_text = """
The customer, who lives near Liberty Market and goes by the nickname "Sunny",
mentioned his brother works at a bank in Gulberg.
"""

results = detect_pii_llm(sample_text)
print(results)