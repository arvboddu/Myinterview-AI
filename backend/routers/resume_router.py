from fastapi import APIRouter, File, UploadFile

from backend.models.request_models import ResumeAnalysisRequest
from backend.services.resume_processor import analyze_resume_file, analyze_resume_text
from backend.services.resume_interview_generator import generate_interview_questions_from_resume


router = APIRouter()


@router.post("/upload")
async def upload(file: UploadFile = File(...)) -> dict:
    return await analyze_resume_file(file)


@router.post("/analyze")
def analyze(req: ResumeAnalysisRequest) -> dict:
    return analyze_resume_text(req.text)


@router.post("/questions")
async def questions_from_resume(file: UploadFile = File(...)) -> dict:
    analysis = await analyze_resume_file(file)
    text = analysis["raw_text"]
    questions = generate_interview_questions_from_resume(text)
    return {"questions": questions}
