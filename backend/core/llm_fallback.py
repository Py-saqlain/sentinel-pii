# backend/core/llm_fallback.py

import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


from config.settings import GROQ_API_KEY, GROQ_MODEL
client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """You are a PII (personally identifiable information) detector.
Given a piece of text, find any personal information that a regex or standard
NLP model might miss — for example, names mentioned casually, addresses written
in unusual formats, or context-dependent sensitive details.

Return ONLY a JSON array, nothing else, no explanation, no markdown formatting.
Each item must have exactly these fields:
- "text": the exact substring found in the input
- "entity_type": a short label like PERSON, ADDRESS, ORGANIZATION, OTHER

If nothing is found, return an empty array: []
"""


def detect_pii_llm(text: str):
    """
    Sends text to Groq and asks it to find PII that regex/Presidio might miss.
    Returns a list of dicts: [{"text": ..., "entity_type": ...}, ...]
    """
    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
            temperature=0,  # deterministic output, not creative
        )

        raw_output = response.choices[0].message.content.strip()
        findings = json.loads(raw_output)
        return findings

    except json.JSONDecodeError:
        # If Groq returns something that isn't valid JSON, fail safely
        # instead of crashing the whole request
        return []
    except Exception as e:
        print(f"LLM fallback error: {e}")
        return []