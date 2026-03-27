from pydantic import BaseModel


class InterviewRequest(BaseModel):
    message: str


class ResumeAnalysisRequest(BaseModel):
    text: str


class TTSRequest(BaseModel):
    text: str


class JobDescriptionRequest(BaseModel):
    text: str


class FeatureRequest(BaseModel):
    request: str
