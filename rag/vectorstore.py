from __future__ import annotations

from pathlib import Path

from rag.embeddings import embed_text
from rag.splitter import split_text


def build_documents(data_dir: Path) -> list[dict]:
    documents: list[dict] = []
    for path in sorted(data_dir.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        for index, chunk in enumerate(split_text(text)):
            documents.append(
                {
                    "id": f"{path.stem}-{index}",
                    "title": path.stem,
                    "content": chunk,
                    "embedding": embed_text(chunk),
                }
            )
    return documents
