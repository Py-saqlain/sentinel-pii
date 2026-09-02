# backend/models/schemas.py

from pydantic import BaseModel
from typing import Literal


class AnonymizeRequest(BaseModel):
    text: str
    strategy: Literal["mask", "replace", "hash"] = "replace"


class AnonymizeResponse(BaseModel):
    original_text: str
    anonymized_text: str
    entities_found: int