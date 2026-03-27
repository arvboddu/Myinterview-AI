from __future__ import annotations

import requests

from backend.config import OLLAMA_HOST


def generate_llm_response(prompt: str, model: str | None = None) -> str:
    selected_model = model or "llama3"
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={"model": selected_model, "prompt": prompt, "stream": False},
            timeout=60,
        )
        response.raise_for_status()
        payload = response.json()
        return payload.get("response") or _fallback_response(prompt)
    except requests.RequestException:
        return _fallback_response(prompt)


def _fallback_response(prompt: str) -> str:
    if "measurable" in prompt.lower():
        return (
            "You explained the scenario clearly. Strengthen the answer by naming the constraint, "
            "your exact contribution, and the measurable outcome."
        )
    return (
        "This is a solid start. Add more specifics about your decision-making, the tradeoffs you "
        "considered, and the final impact."
    )
