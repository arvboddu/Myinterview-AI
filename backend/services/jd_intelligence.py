from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import uuid

from fastapi import UploadFile
from backend.services.ollama_client import generate_llm_response
from backend.services.rag_client import add_text_document
from backend.services.resume_processor import clean, extract_text


SKILL_HINTS = {
    "ownership": ["own", "ownership", "accountable", "end-to-end"],
    "delivery excellence": ["delivery", "execution", "release", "milestone", "timeline"],
    "prioritization": ["prioritize", "roadmap", "tradeoff", "backlog"],
    "conflict resolution": ["conflict", "alignment", "escalation", "resolve"],
    "stakeholder alignment": ["stakeholder", "cross-functional", "partner", "alignment"],
    "program execution": ["program", "dependency", "risk", "planning", "execution"],
}


@dataclass
class JobDescriptionProfile:
    responsibilities: list[str]
    requirements: list[str]
    skills: list[str]
    kpis: list[str]
    competencies: list[str]
    tools: list[str]
    team_structure: list[str]
    skill_matrix: dict[str, str]
    question_categories: dict[str, list[str]]
    scenarios: list[str]
    rubric: list[str]
    summary: str

    def to_dict(self) -> dict:
        return {
            "responsibilities": self.responsibilities,
            "requirements": self.requirements,
            "skills": self.skills,
            "kpis": self.kpis,
            "competencies": self.competencies,
            "tools": self.tools,
            "team_structure": self.team_structure,
            "skill_matrix": self.skill_matrix,
            "question_categories": self.question_categories,
            "scenarios": self.scenarios,
            "rubric": self.rubric,
            "summary": self.summary,
        }


def analyze_job_description(text: str) -> dict:
    lines = _normalize_lines(text)
    responsibilities = _extract_section(lines, ["respons", "own", "lead", "deliver"])
    requirements = _extract_section(lines, ["require", "experience", "must", "qualif"])
    kpis = _extract_section(lines, ["kpi", "metric", "goal", "outcome", "sla", "%"])
    tools = _extract_keywords(text, ["jira", "sql", "python", "excel", "tableau", "asana", "confluence", "aws"])
    competencies = _derive_competencies(text)
    skills = sorted(set(competencies + _extract_keywords(text, ["stakeholder", "roadmap", "delivery", "program", "execution", "risk", "agile", "scrum"])))
    team_structure = _extract_section(lines, ["team", "partner", "cross-functional", "engineering", "design", "operations"])
    skill_matrix = _build_skill_matrix(text)
    question_categories = _build_question_categories(responsibilities, competencies)
    scenarios = _build_scenarios(responsibilities, competencies)
    rubric = _build_rubric(competencies, kpis)
    summary = _generate_summary(text, responsibilities, competencies)

    profile = JobDescriptionProfile(
        responsibilities=responsibilities[:8],
        requirements=requirements[:8],
        skills=skills[:10],
        kpis=kpis[:6],
        competencies=competencies[:8],
        tools=tools[:8],
        team_structure=team_structure[:6],
        skill_matrix=skill_matrix,
        question_categories=question_categories,
        scenarios=scenarios[:6],
        rubric=rubric[:8],
        summary=summary,
    )
    return profile.to_dict()


def generate_interview_from_jd(text: str) -> dict:
    profile = analyze_job_description(text)
    add_text_document("job_description_profile", text)
    for category, questions in profile["question_categories"].items():
        add_text_document(f"jd_{category}", "\n".join(questions))

    opening_prompt = (
        f"Start a PM-delivery interview focused on {', '.join(profile['competencies'][:3])}. "
        f"Lean on responsibilities like {', '.join(profile['responsibilities'][:2]) or 'program delivery'}."
    )
    return {
        "profile": profile,
        "opening_prompt": opening_prompt,
        "recommended_mode": "role_based_interview",
    }


async def analyze_job_description_file(file: UploadFile) -> dict:
    raw_text = await extract_uploaded_jd_text(file)
    profile = analyze_job_description(raw_text)
    return {
        "raw_text": raw_text,
        "profile": profile,
    }


async def generate_interview_from_jd_file(file: UploadFile) -> dict:
    raw_text = await extract_uploaded_jd_text(file)
    result = generate_interview_from_jd(raw_text)
    result["raw_text"] = raw_text
    return result


async def extract_uploaded_jd_text(file: UploadFile) -> str:
    suffix = Path(file.filename or "job_description.txt").suffix or ".txt"
    temp_path = Path(f"jd_{uuid.uuid4()}{suffix}")
    temp_path.write_bytes(await file.read())
    try:
        return clean(extract_text(temp_path))
    finally:
        if temp_path.exists():
            os.remove(temp_path)


def _normalize_lines(text: str) -> list[str]:
    return [line.strip("-* \t") for line in text.splitlines() if line.strip()]


def _extract_section(lines: list[str], hints: list[str]) -> list[str]:
    matches = []
    for line in lines:
        lowered = line.lower()
        if any(hint in lowered for hint in hints):
            matches.append(line)
    return matches


def _extract_keywords(text: str, candidates: list[str]) -> list[str]:
    lowered = text.lower()
    found = [item for item in candidates if item in lowered]
    return [item.title() for item in found]


def _derive_competencies(text: str) -> list[str]:
    lowered = text.lower()
    found = []
    for competency, hints in SKILL_HINTS.items():
        if any(hint in lowered for hint in hints):
            found.append(competency.title())
    if not found:
        found = ["Ownership", "Delivery Excellence", "Stakeholder Alignment"]
    return found


def _build_skill_matrix(text: str) -> dict[str, str]:
    lowered = text.lower()
    matrix = {}
    for competency, hints in SKILL_HINTS.items():
        if any(hint in lowered for hint in hints):
            level = "high" if sum(hint in lowered for hint in hints) >= 2 else "medium"
            matrix[competency.title()] = level
    if not matrix:
        matrix = {"Ownership": "medium", "Delivery Excellence": "medium"}
    return matrix


def _build_question_categories(responsibilities: list[str], competencies: list[str]) -> dict[str, list[str]]:
    lead_responsibility = responsibilities[0] if responsibilities else "a complex delivery program"
    return {
        "behavioral_questions": [
            f"Tell me about a time you showed strong {competencies[0] if competencies else 'ownership'} in {lead_responsibility}.",
            "Describe a situation where you had to align conflicting stakeholders.",
        ],
        "delivery_questions": [
            "How do you keep a multi-team delivery program on track when dependencies slip?",
            "What signals tell you a release plan needs intervention?",
        ],
        "leadership_questions": [
            "How do you drive accountability without direct authority?",
            "Describe how you coach teams through ambiguous execution risk.",
        ],
        "execution_questions": [
            "How do you break down a strategic goal into delivery milestones?",
            "How do you decide what to cut when timelines compress?",
        ],
        "risk_mitigation_questions": [
            "Tell me about a delivery risk you spotted early and how you handled it.",
            "How do you surface and escalate blockers before they become incidents?",
        ],
        "follow_up_questions": [
            "What tradeoff did you make?",
            "What metric changed because of your intervention?",
        ],
    }


def _build_scenarios(responsibilities: list[str], competencies: list[str]) -> list[str]:
    lead = responsibilities[0] if responsibilities else "a cross-functional program"
    focus = competencies[0] if competencies else "delivery excellence"
    return [
        f"You are leading {lead} and two partner teams disagree on scope. Walk through your plan.",
        f"A KPI is slipping during a launch. How do you apply {focus} to recover the program?",
        "A stakeholder asks for last-minute scope without moving the date. What do you do?",
    ]


def _build_rubric(competencies: list[str], kpis: list[str]) -> list[str]:
    rubric = ["clarity", "ownership", "decision-making", "stakeholder management"]
    rubric.extend(item.lower() for item in competencies[:3])
    if kpis:
        rubric.append("metric orientation")
    return list(dict.fromkeys(rubric))


def _generate_summary(text: str, responsibilities: list[str], competencies: list[str]) -> str:
    prompt = (
        "Summarize this job description in 4 concise bullet-style sentences for a PM-delivery interview coach.\n"
        f"Responsibilities: {responsibilities}\n"
        f"Competencies: {competencies}\n"
        f"Text: {text[:3000]}"
    )
    return generate_llm_response(prompt)
