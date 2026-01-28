import json
from typing import Dict, Any, List
from src.llm import ollama_generate

LABELS: List[str] = ["urgent", "action_required", "informational", "spam", "personal"]

SYSTEM_RULES = """
You are an email classifier.
Return ONLY valid JSON with keys:
- label: one of ["urgent","action_required","informational","spam","personal"]
- confidence: number from 0.0 to 1.0
- reason: short string (max 20 words)
No extra text.
"""

def trim_email(text: str, max_chars: int = 1500) -> str:
    if not text:
        return ""
    #cut off common reply separators
    cut_markers = ["\nOn ", "\nFrom:", "\n-----Original Message-----", "\n> "]
    for m in cut_markers:
        idx = text.find(m)
        if idx != -1 and idx > 200:
            text = text[:idx]
            break
    return text.strip()[:max_chars]


def classify_email(model: str, email: Dict[str, str]) -> Dict[str, Any]:
    prompt = f"""{SYSTEM_RULES}

Email:
From: {email.get("from","")}
Subject: {email.get("subject","")}
Body:
{trim_email(email.get("text",""))}
"""
    raw = ollama_generate(model=model, prompt=prompt, temperature=0.1)

    
    try:
        return json.loads(raw)
    except Exception:
        # Fallback if model adds junk
        start = raw.find("{")
        end = raw.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(raw[start:end+1])
        raise
