from __future__ import annotations

import uuid
from pathlib import Path


def synthesize_speech(text: str) -> Path:
    output_dir = Path("generated_audio")
    output_dir.mkdir(exist_ok=True)
    filename = output_dir / f"tts_{uuid.uuid4()}.wav"
    filename.write_bytes(f"Placeholder audio for: {text[:120]}".encode("utf-8"))
    return filename
