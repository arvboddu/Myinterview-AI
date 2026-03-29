"""
Live Interview Copilot Service
Handles all interview copilot functionality
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime
from typing import Any

from backend.services.copilot_prompts import (
    get_live_answer_prompt,
    get_prompt,
    get_tone_adapted_prompt,
    get_length_formatted_prompt,
    get_transcription_cleaned_prompt,
)
from backend.services.ollama_client import generate_llm_response


class CopilotSession:
    """Represents a copilot interview session."""

    def __init__(
        self,
        session_id: str,
        resume: dict | None = None,
        jd: str = "",
        role: str = "Product Manager",
        language: str = "en",
        model: str = "gpt-5",
        tone: str = "professional",
        format: str = "paragraph",
        thinking_mode: bool = False,
        materials: list[str] | None = None,
    ):
        self.session_id = session_id
        self.resume = resume or {}
        self.jd = jd
        self.role = role
        self.language = language
        self.model = model
        self.tone = tone
        self.format = format
        self.thinking_mode = thinking_mode
        self.materials = materials or []
        self.created_at = datetime.now()
        self.conversation_history: list[dict] = []

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "resume": self.resume,
            "jd": self.jd,
            "role": self.role,
            "language": self.language,
            "model": self.model,
            "tone": self.tone,
            "format": self.format,
            "thinking_mode": self.thinking_mode,
            "materials": self.materials,
            "created_at": self.created_at.isoformat(),
            "conversation_history": self.conversation_history,
        }


class CopilotService:
    """Service for managing interview copilot sessions."""

    def __init__(self):
        self.sessions: dict[str, CopilotSession] = {}

    def create_session(
        self,
        resume: dict | None = None,
        jd: str = "",
        role: str = "Product Manager",
        language: str = "en",
        model: str = "gpt-5",
        tone: str = "professional",
        format: str = "paragraph",
        thinking_mode: bool = False,
        materials: list[str] | None = None,
    ) -> dict:
        session_id = str(uuid.uuid4())
        session = CopilotSession(
            session_id=session_id,
            resume=resume,
            jd=jd,
            role=role,
            language=language,
            model=model,
            tone=tone,
            format=format,
            thinking_mode=thinking_mode,
            materials=materials,
        )
        self.sessions[session_id] = session
        return {
            "session_id": session_id,
            "status": "ready",
            "message": "Session initialized. Ready to receive interview questions.",
            "config": {
                "role": role,
                "language": language,
                "model": model,
                "tone": tone,
                "format": format,
                "thinking_mode": thinking_mode,
            },
        }

    def get_session(self, session_id: str) -> CopilotSession | None:
        return self.sessions.get(session_id)

    def delete_session(self, session_id: str) -> bool:
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False

    def generate_answer(self, session_id: str, question: str) -> dict:
        session = self.get_session(session_id)
        if not session:
            return {"error": "Session not found"}

        prompt = get_live_answer_prompt(
            resume_json=session.resume,
            jd_text=session.jd,
            role=session.role,
            language=session.language,
            tone=session.tone,
            format=session.format,
            thinking_mode=session.thinking_mode,
            question=question,
            materials=session.materials,
        )

        try:
            answer = generate_llm_response(
                prompt, model=session.model, timeout=60, max_tokens=1000
            )
        except Exception:
            answer = self._fallback_answer(question, session.tone)

        session.conversation_history.append(
            {
                "question": question,
                "answer": answer,
                "timestamp": datetime.now().isoformat(),
            }
        )

        return {
            "answer": answer,
            "question": question,
            "session_id": session_id,
            "config_used": {
                "tone": session.tone,
                "format": session.format,
                "thinking_mode": session.thinking_mode,
                "model": session.model,
            },
        }

    def clean_transcription(self, raw_transcript: str) -> dict:
        prompt = get_transcription_cleaned_prompt(raw_transcript)
        try:
            cleaned = generate_llm_response(prompt, timeout=30, max_tokens=500)
        except Exception:
            cleaned = raw_transcript

        return {"cleaned_transcript": cleaned, "raw_transcript": raw_transcript}

    def adapt_tone(self, answer: str, tone: str) -> dict:
        prompt = get_tone_adapted_prompt(answer, tone)
        try:
            adapted = generate_llm_response(prompt, timeout=30, max_tokens=1000)
        except Exception:
            adapted = answer

        return {"original": answer, "adapted": adapted, "tone": tone}

    def format_length(self, answer: str, format: str) -> dict:
        prompt = get_length_formatted_prompt(answer, format)
        try:
            formatted = generate_llm_response(prompt, timeout=30, max_tokens=1000)
        except Exception:
            formatted = answer

        return {"original": answer, "formatted": formatted, "format": format}

    def parse_resume(self, resume_text: str) -> dict:
        prompt = get_prompt("resume_parser", resume_text=resume_text)
        result = None
        try:
            result = generate_llm_response(prompt, timeout=60, max_tokens=2000)
            parsed = json.loads(result)
        except json.JSONDecodeError:
            parsed = (
                {"error": "Failed to parse resume", "raw": result}
                if result
                else {"error": "Failed to parse resume"}
            )
        except Exception as e:
            parsed = {"error": f"Failed to process resume: {str(e)}"}

        return parsed

    def analyze_job_description(self, jd_text: str, resume_summary: str = "") -> dict:
        prompt = get_prompt(
            "job_description_analysis", jd_text=jd_text, resume_summary=resume_summary
        )
        try:
            result = generate_llm_response(prompt, timeout=60, max_tokens=1500)
            analysis = json.loads(result)
        except json.JSONDecodeError:
            analysis = {"error": "Failed to analyze job description", "raw": result}
        except Exception:
            analysis = {"error": "Failed to process job description"}

        return analysis

    def _fallback_answer(self, question: str, tone: str) -> str:
        tone_prefixes = {
            "professional": "Based on my experience, ",
            "assertive": "I decisively handled this by ",
            "friendly": "Honestly, it was a great learning experience when ",
        }

        prefix = tone_prefixes.get(tone, "")

        if "leadership" in question.lower():
            return f"{prefix}demonstrating leadership by guiding my team through challenges, setting clear expectations, and ensuring accountability while supporting individual growth and team success."
        elif "challenge" in question.lower() or "difficult" in question.lower():
            return f"{prefix}identifying the core issue, prioritizing solutions, and collaborating with stakeholders to implement an effective resolution while maintaining focus on key objectives."
        elif "success" in question.lower() or "achievement" in question.lower():
            return f"{prefix}delivering measurable results through strategic planning, cross-functional collaboration, and data-driven decision-making that aligned with organizational goals."
        elif "conflict" in question.lower() or "disagree" in question.lower():
            return f"{prefix}addressing disagreements by first understanding all perspectives, then facilitating a constructive dialogue focused on shared goals and mutual resolution."
        else:
            return f"{prefix}taking a structured approach to analyze the situation, develop options, and implement a solution that balances stakeholder needs with practical constraints."


copilot_service = CopilotService()
