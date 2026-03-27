from fastapi import APIRouter

from backend.services.rag_client import retrieve_context


router = APIRouter()


@router.get("/search")
def search(q: str) -> dict:
    return {"context": retrieve_context(q)}
