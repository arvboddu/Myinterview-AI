"""
Copilot Router - Live Interview Copilot API endpoints
"""

from fastapi import APIRouter, HTTPException

from backend.services.copilot_service import copilot_service


router = APIRouter(tags=["copilot"])


@router.post("/create-session")
def create_copilot_session(req: dict) -> dict:
    """Create a new interview copilot session."""
    return copilot_service.create_session(
        resume=req.get("resume"),
        jd=req.get("jd", ""),
        role=req.get("role", "Product Manager"),
        language=req.get("language", "en"),
        model=req.get("model", "gpt-5"),
        tone=req.get("tone", "professional"),
        format=req.get("format", "paragraph"),
        thinking_mode=req.get("thinking_mode", False),
        materials=req.get("materials", []),
    )


@router.post("/generate-answer")
def generate_copilot_answer(req: dict) -> dict:
    """Generate an answer for an interview question."""
    session_id = req.get("session_id")
    question = req.get("question")

    if not session_id:
        raise HTTPException(status_code=400, detail="session_id is required")
    if not question:
        raise HTTPException(status_code=400, detail="question is required")

    result = copilot_service.generate_answer(session_id, question)

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return result


@router.post("/clean-transcription")
def clean_transcription(req: dict) -> dict:
    """Clean raw speech-to-text transcription."""
    raw_transcript = req.get("raw_transcript", "")
    return copilot_service.clean_transcription(raw_transcript)


@router.post("/adapt-tone")
def adapt_answer_tone(req: dict) -> dict:
    """Adapt an answer to a different tone."""
    answer = req.get("answer", "")
    tone = req.get("tone", "professional")

    if not answer:
        raise HTTPException(status_code=400, detail="answer is required")

    return copilot_service.adapt_tone(answer, tone)


@router.post("/format-answer")
def format_answer_length(req: dict) -> dict:
    """Format an answer to a different length."""
    answer = req.get("answer", "")
    format_type = req.get("format", "paragraph")

    if not answer:
        raise HTTPException(status_code=400, detail="answer is required")

    return copilot_service.format_length(answer, format_type)


@router.post("/parse-resume")
def parse_resume(req: dict) -> dict:
    """Parse a resume into structured JSON."""
    resume_text = req.get("resume_text", "")

    if not resume_text:
        raise HTTPException(status_code=400, detail="resume_text is required")

    return copilot_service.parse_resume(resume_text)


@router.post("/analyze-jd")
def analyze_job_description(req: dict) -> dict:
    """Analyze a job description."""
    jd_text = req.get("jd_text", "")
    resume_summary = req.get("resume_summary", "")

    if not jd_text:
        raise HTTPException(status_code=400, detail="jd_text is required")

    return copilot_service.analyze_job_description(jd_text, resume_summary)


@router.get("/session/{session_id}")
def get_copilot_session(session_id: str) -> dict:
    """Get session details."""
    session = copilot_service.get_session(session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return session.to_dict()


@router.delete("/session/{session_id}")
def delete_copilot_session(session_id: str) -> dict:
    """Delete a copilot session."""
    if copilot_service.delete_session(session_id):
        return {"status": "deleted", "session_id": session_id}
    raise HTTPException(status_code=404, detail="Session not found")
