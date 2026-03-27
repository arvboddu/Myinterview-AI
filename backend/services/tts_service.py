from __future__ import annotations

import uuid
from pathlib import Path

import requests

from backend.config import TTS_HOST


def synthesize_speech(text: str) -> str:
    filename = Path("generated_audio") / f"tts_{uuid.uuid4()}.wav"
    filename.parent.mkdir(exist_ok=True)

    try:
        response = requests.post(f"{TTS_HOST}/api/tts", json={"text": text}, timeout=30)
        response.raise_for_status()
        filename.write_bytes(response.content)
    except requests.RequestException:
        filename.write_bytes(f"Placeholder audio for: {text[:120]}".encode("utf-8"))

    return str(filename)
