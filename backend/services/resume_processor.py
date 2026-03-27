from __future__ import annotations

import os
import re
import uuid
from pathlib import Path

from fastapi import UploadFile
from backend.services.ollama_client import generate_llm_response

try:
    import docx2txt
except ImportError:
    docx2txt = None

try:
    import pdfplumber
except ImportError:
    pdfplumber = None


def extract_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf" and pdfplumber is not None:
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += " " + (page.extract_text() or "")
        return text
    if suffix == ".docx" and docx2txt is not None:
        return docx2txt.process(str(path))
    if suffix == ".txt":
        return path.read_text(encoding="utf-8", errors="ignore")
    if suffix in {".md", ".py"}:
        return path.read_text(encoding="utf-8", errors="ignore")
    return path.read_text(encoding="utf-8", errors="ignore")


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


async def analyze_resume_file(file: UploadFile) -> dict:
    suffix = Path(file.filename or "resume.txt").suffix or ".txt"
    temp_path = Path(f"tmp_{uuid.uuid4()}{suffix}")
    temp_path.write_bytes(await file.read())
    try:
        raw_text = clean(extract_text(temp_path))
        analysis = analyze_resume_text(raw_text)
        return {
            "raw_text": raw_text,
            "analysis": analysis["analysis"],
        }
    finally:
        if temp_path.exists():
            os.remove(temp_path)


def analyze_resume_text(text: str) -> dict:
    prompt = (
        f"""
Analyze the following resume:
{text}
Return JSON with strengths, achievements, gaps, and delivery skills.
"""
    )
    response = generate_llm_response(prompt)
    return {"analysis": response}
