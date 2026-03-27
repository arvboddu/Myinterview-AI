from __future__ import annotations

import re


def plan_feature(request: str) -> dict:
    slug = _slugify(request)
    feature_type = _infer_feature_type(request)
    backend_route = f"/api/features/{slug}"
    service_file = f"backend/services/{slug}.py"

    return {
        "feature_name": slug,
        "feature_type": feature_type,
        "summary": request.strip(),
        "backend_route": backend_route,
        "service_file": service_file,
        "frontend_tab": _titleize(slug),
        "interview_engine_changes": "Extend interview engine" if any(token in request.lower() for token in ["interview", "simulation", "roleplay"]) else "No direct interview engine change required",
        "rag_integration": any(token in request.lower() for token in ["knowledge", "document", "search", "rag", "context"]),
        "generated_plan": [
            f"Create route {backend_route}",
            f"Implement logic in {service_file}",
            "Add frontend controls and result panel",
            "Add tests for request and response flow",
            "Update README and helper scripts if the feature adds a user-facing route",
        ],
    }


def _slugify(text: str) -> str:
    words = re.findall(r"[a-zA-Z0-9]+", text.lower())
    return "_".join(words[:5]) or "new_feature"


def _infer_feature_type(text: str) -> str:
    lowered = text.lower()
    if any(token in lowered for token in ["simulate", "simulation", "roleplay", "interview"]):
        return "interaction-driven"
    if any(token in lowered for token in ["document", "knowledge", "search", "rag"]):
        return "knowledge-driven"
    if any(token in lowered for token in ["score", "analyze", "matrix"]):
        return "analysis"
    return "general_extension"


def _titleize(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.split("_"))
