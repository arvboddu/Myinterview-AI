from fastapi import APIRouter

from backend.models.request_models import InterviewRequest
from backend.services.interview_engine import InterviewEngine
from backend.services.rag_client import retrieve_context


router = APIRouter()
engine = InterviewEngine()

@router.post("/interview")
def interview_user(req: InterviewRequest) -> dict:
    context = retrieve_context(req.message)
    response = engine.generate(req.message, context)
    return {"response": response}


@router.post("/reset")
def reset_interview() -> dict:
    engine.reset()
    return {"status": "reset"}
