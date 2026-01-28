import json
import requests
from typing import Dict, Any

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

def ollama_generate(model: str, prompt: str, temperature: float = 0.2) -> str:
    payload: Dict[str, Any] = {
        "model": model,
        "prompt": prompt,
        "stream": True,  # stream so we don't hit read timeouts
        "options": {"temperature": temperature},
    }

    # (connect timeout, read timeout) — read timeout is None because we stream chunks
    with requests.post(OLLAMA_URL, json=payload, stream=True, timeout=(10, None)) as r:
        r.raise_for_status()

        chunks = []
        for line in r.iter_lines(decode_unicode=True):
            if not line:
                continue
            obj = json.loads(line)
            if "response" in obj:
                chunks.append(obj["response"])
            if obj.get("done"):
                break

    return "".join(chunks).strip()
