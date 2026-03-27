from fastapi import APIRouter, File, UploadFile

from backend.models.request_models import JobDescriptionRequest
from backend.routers.interview_router import engine
from backend.services.jd_intelligence import (
    analyze_job_description,
    analyze_job_description_file,
    generate_interview_from_jd,
    generate_interview_from_jd_file,
)


router = APIRouter()


@router.post("/analyze")
def analyze_jd(req: JobDescriptionRequest) -> dict:
    return analyze_job_description(req.text)


@router.post("/generate-interview")
def generate_jd_interview(req: JobDescriptionRequest) -> dict:
    result = generate_interview_from_jd(req.text)
    engine.set_job_description_profile(result["profile"])
    return result


@router.post("/analyze-upload")
async def analyze_jd_upload(file: UploadFile = File(...)) -> dict:
    return await analyze_job_description_file(file)


@router.post("/generate-interview-upload")
async def generate_jd_interview_upload(file: UploadFile = File(...)) -> dict:
    result = await generate_interview_from_jd_file(file)
    engine.set_job_description_profile(result["profile"])
    return result
