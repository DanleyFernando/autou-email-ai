from pydantic import BaseModel
from typing import Dict

class ProcessResponse(BaseModel):
    category: str
    confidence: float
    suggested_reply: str
    meta: Dict
