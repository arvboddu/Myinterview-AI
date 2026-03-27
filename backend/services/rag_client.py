from __future__ import annotations

from collections import Counter
from math import sqrt
from pathlib import Path

from backend.config import CHROMA_PATH

try:
    import chromadb
except ImportError:
    chromadb = None


DATA_DIR = Path(__file__).resolve().parents[2] / "data"
SEED_FILE = DATA_DIR / "interview_notes.txt"

if chromadb is not None:
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection("pm_ai_docs")
else:
    client = None
    collection = None


def retrieve_context(query: str, n: int = 3) -> str:
    if collection is not None:
        try:
            results = collection.query(query_texts=[query], n_results=n)
            if results and results.get("documents"):
                documents = results["documents"][0]
                if documents:
                    joined = "\n".join(item for item in documents if item)
                    if joined.strip():
                        return joined
        except Exception:
            pass

    documents = _load_documents()
    if not documents:
        return ""
    query_vector = _embed(query)
    ranked = sorted(
        documents,
        key=lambda item: _cosine_similarity(query_vector, item["embedding"]),
        reverse=True,
    )
    return "\n".join(item["content"] for item in ranked[:n])


def add_text_document(name: str, text: str) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    file_path = DATA_DIR / f"{name}.txt"
    file_path.write_text(text, encoding="utf-8")
    if collection is not None:
        try:
            chunks = [chunk.strip() for chunk in text.split(". ") if chunk.strip()]
            if chunks:
                ids = [f"{name}-{index}" for index, _ in enumerate(chunks)]
                collection.upsert(documents=chunks, ids=ids)
        except Exception:
            pass


def _load_documents() -> list[dict]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not SEED_FILE.exists():
        SEED_FILE.write_text(
            (
                "Strong interview answers explain the situation, constraints, action, and result. "
                "For technical rounds, discuss tradeoffs, failure modes, and why your approach was "
                "appropriate. For leadership and behavioral rounds, show ownership, collaboration, "
                "and the measurable outcome."
            ),
            encoding="utf-8",
        )
    content = SEED_FILE.read_text(encoding="utf-8")
    chunks = [chunk.strip() for chunk in content.split(". ") if chunk.strip()]
    return [{"content": chunk, "embedding": _embed(chunk)} for chunk in chunks]


def _embed(text: str) -> Counter:
    tokens = [token.strip(".,:;!?").lower() for token in text.split() if token.strip()]
    return Counter(tokens)


def _cosine_similarity(left: Counter, right: Counter) -> float:
    if not left or not right:
        return 0.0
    overlap = set(left) & set(right)
    numerator = sum(left[token] * right[token] for token in overlap)
    left_norm = sqrt(sum(value * value for value in left.values()))
    right_norm = sqrt(sum(value * value for value in right.values()))
    if not left_norm or not right_norm:
        return 0.0
    return numerator / (left_norm * right_norm)
