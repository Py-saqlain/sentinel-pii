# backend/tests/test_detector.py

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.detector import detect_pii

sample_text = """
My name is Ahmed Khan and my CNIC is 35202-1234567-1.
You can reach me at 0300-1234567 or my office at 042-35761234.
My email is ahmed.khan@example.com
"""

results = detect_pii(sample_text)

for r in results:
    detected_text = sample_text[r.start:r.end]
    print(f"Found: '{detected_text}' | Type: {r.entity_type} | Score: {r.score:.2f}")