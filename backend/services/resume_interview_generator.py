import ast
import json

from backend.services.ollama_client import generate_llm_response


def generate_interview_questions_from_resume(text: str) -> dict:
    prompt = f"""
Generate PM-Delivery interview questions tailored to this resume:
{text}
Return JSON with:
- behavioral_questions
- delivery_questions
- leadership_questions
- execution_questions
- risk_mitigation_questions
- follow_up_questions
"""
    response = generate_llm_response(prompt)
    parsed = _parse_generated_output(response)
    if parsed is not None:
        return _normalize_question_payload(parsed)
    return _fallback_question_set(text, response)


def _parse_generated_output(response: str) -> dict | None:
    try:
        return json.loads(response)
    except Exception:
        pass

    try:
        parsed = ast.literal_eval(response)
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        return None
    return None


def _normalize_question_payload(payload: dict) -> dict:
    categories = [
        "behavioral_questions",
        "delivery_questions",
        "leadership_questions",
        "execution_questions",
        "risk_mitigation_questions",
        "follow_up_questions",
    ]
    normalized = {}
    for category in categories:
        value = payload.get(category, [])
        if isinstance(value, str):
            normalized[category] = [value]
        elif isinstance(value, list):
            normalized[category] = [item for item in value if isinstance(item, str) and item.strip()]
        else:
            normalized[category] = []

    if any(normalized.values()):
        return normalized
    return _fallback_question_set("", "")


def _fallback_question_set(text: str, response: str) -> dict:
    focus = "delivery ownership"
    lowered = text.lower()
    if "stakeholder" in lowered:
        focus = "stakeholder alignment"
    elif "risk" in lowered:
        focus = "risk mitigation"
    elif "roadmap" in lowered:
        focus = "roadmap prioritization"

    return {
        "behavioral_questions": [
            f"Tell me about a time you demonstrated strong {focus} in a high-pressure situation.",
            "Describe a project where you had to influence without direct authority.",
        ],
        "delivery_questions": [
            "How did you keep a cross-functional initiative on track when a dependency slipped?",
            "What metrics did you use to know your delivery plan was healthy?",
        ],
        "leadership_questions": [
            "How do you build trust with engineering, design, and business stakeholders?",
            "Describe how you handled disagreement on scope or priority.",
        ],
        "execution_questions": [
            "How do you break a broad objective into milestones and checkpoints?",
            "What tradeoffs do you make when timelines compress?",
        ],
        "risk_mitigation_questions": [
            "Tell me about a risk you identified early and how you managed it.",
            "How do you escalate blockers without creating unnecessary churn?",
        ],
        "follow_up_questions": [
            "What was your exact contribution?",
            "What measurable outcome changed because of your actions?",
        ],
        "notes": response.strip() or "Generated from local fallback because the LLM did not return structured JSON.",
    }
