from __future__ import annotations

import subprocess

from backend.config import WHISPER_BIN


def transcribe_audio(path: str) -> str:
    try:
        result = subprocess.run(
            [WHISPER_BIN, path, "--model", "base.en"],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.stdout.strip() or ""
    except OSError:
        return ""
