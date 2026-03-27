from __future__ import annotations

import json
from pathlib import Path

from rag.vectorstore import build_documents


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    data_dir = root / "data"
    output = root / "data" / "rag_index.json"
    data_dir.mkdir(parents=True, exist_ok=True)

    seed_file = data_dir / "interview_notes.txt"
    if not seed_file.exists():
        seed_file.write_text(
            (
                "Strong interview answers explain the situation, constraints, action, and result. "
                "For technical rounds, discuss tradeoffs, failure modes, and why your approach was appropriate. "
                "For leadership and behavioral rounds, show ownership, collaboration, and the measurable outcome."
            ),
            encoding="utf-8",
        )

    documents = build_documents(data_dir)
    serializable = [
        {"id": item["id"], "title": item["title"], "content": item["content"]}
        for item in documents
    ]
    output.write_text(json.dumps(serializable, indent=2), encoding="utf-8")
    print(f"Wrote {len(serializable)} chunks to {output}")


if __name__ == "__main__":
    main()
