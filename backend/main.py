from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.routers import feature_router, interview_router, jd_router, rag_router, resume_router, voice_router


app = FastAPI(
    title="MyInterview AI Backend",
    description="Local interview simulator for JD-aware practice, resume review, and feature planning",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(interview_router.router, prefix="/api")
app.include_router(feature_router.router, prefix="/api/features")
app.include_router(jd_router.router, prefix="/api/jd")
app.include_router(resume_router.router, prefix="/api/resume")
app.include_router(voice_router.router, prefix="/api/voice")
app.include_router(rag_router.router, prefix="/api/rag")
app.mount("/generated_audio", StaticFiles(directory="generated_audio"), name="generated_audio")


@app.get("/")
def root() -> dict:
    return {"status": "MyInterview AI Backend Running"}


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
