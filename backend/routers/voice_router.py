import os
import uuid
from pathlib import Path

from fastapi import APIRouter, File, UploadFile

from backend.models.request_models import TTSRequest
from backend.services.tts_service import synthesize_speech
from backend.services.whisper_stt import transcribe_audio


router = APIRouter()

@router.post("/stt")
async def stt(file: UploadFile = File(...)) -> dict:
    suffix = Path(file.filename or "audio.wav").suffix or ".wav"
    temp_path = Path(f"temp_{uuid.uuid4()}{suffix}")
    temp_path.write_bytes(await file.read())
    try:
        text = transcribe_audio(temp_path)
        return {"text": text}
    finally:
        if temp_path.exists():
            os.remove(temp_path)


@router.post("/tts")
def tts(data: TTSRequest) -> dict:
    audio_file = synthesize_speech(data.text)
    return {"audio_file": audio_file}
