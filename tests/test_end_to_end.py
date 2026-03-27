import io
import unittest
import wave
from pathlib import Path

from fastapi.testclient import TestClient

from backend.main import app
from backend.routers.interview_router import engine


SAMPLE_INTERVIEW_MESSAGE = "Ask me a PM-delivery interview question about release risk."
SAMPLE_RESUME_TEXT = """
Senior Product Manager with end-to-end delivery ownership across roadmap planning,
stakeholder alignment, launch readiness, KPI tracking, and execution risk mitigation.
Led cross-functional teams across engineering, design, and operations.
"""
SAMPLE_JOB_DESCRIPTION = """
Product Manager - Delivery

Responsibilities:
- Lead cross-functional delivery planning across engineering, design, analytics, and operations.
- Own release milestones, execution risk tracking, and stakeholder communication.
- Drive KPI reporting, launch readiness, and dependency management.

Requirements:
- 5+ years of product management or program delivery experience.
- Strong stakeholder alignment, roadmap prioritization, and risk mitigation skills.
- Experience with Jira, SQL, Confluence, and Agile execution.
"""


def _sample_text_upload(name: str, text: str) -> tuple[str, io.BytesIO, str]:
    return (name, io.BytesIO(text.encode("utf-8")), "text/plain")


def _sample_wav_upload(name: str = "sample.wav") -> tuple[str, io.BytesIO, str]:
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(16000)
        wav_file.writeframes(b"\x00\x00" * 1600)
    buffer.seek(0)
    return (name, buffer, "audio/wav")


class EndToEndApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls) -> None:
        engine.reset()

    def setUp(self) -> None:
        engine.reset()

    def test_health_endpoint(self) -> None:
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_interview_and_reset_flow(self) -> None:
        interview_response = self.client.post("/api/interview", json={"message": SAMPLE_INTERVIEW_MESSAGE})

        self.assertEqual(interview_response.status_code, 200)
        payload = interview_response.json()
        self.assertIn("response", payload)
        self.assertTrue(payload["response"].strip())
        self.assertEqual(len(engine.history), 1)

        reset_response = self.client.post("/api/reset")

        self.assertEqual(reset_response.status_code, 200)
        self.assertEqual(reset_response.json()["status"], "reset")
        self.assertEqual(engine.history, [])
        self.assertIsNone(engine.job_description_profile)

    def test_resume_text_analysis(self) -> None:
        response = self.client.post("/api/resume/analyze", json={"text": SAMPLE_RESUME_TEXT})

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("analysis", payload)
        self.assertTrue(payload["analysis"].strip())

    def test_resume_upload_analysis(self) -> None:
        response = self.client.post(
            "/api/resume/upload",
            files={"file": _sample_text_upload("resume.txt", SAMPLE_RESUME_TEXT)},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("raw_text", payload)
        self.assertIn("analysis", payload)
        self.assertIn("stakeholder alignment", payload["raw_text"].lower())
        self.assertTrue(payload["analysis"].strip())

    def test_resume_question_generation(self) -> None:
        response = self.client.post(
            "/api/resume/questions",
            files={"file": _sample_text_upload("resume.txt", SAMPLE_RESUME_TEXT)},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("questions", payload)
        questions = payload["questions"]
        for key in [
            "behavioral_questions",
            "delivery_questions",
            "leadership_questions",
            "execution_questions",
            "risk_mitigation_questions",
            "follow_up_questions",
        ]:
            self.assertIn(key, questions)
            self.assertTrue(questions[key])

    def test_rag_search_returns_context(self) -> None:
        response = self.client.get("/api/rag/search", params={"q": "stakeholder management"})

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("context", payload)
        self.assertTrue(payload["context"].strip())

    def test_job_description_text_analysis(self) -> None:
        response = self.client.post("/api/jd/analyze", json={"text": SAMPLE_JOB_DESCRIPTION})

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload["summary"].strip())
        self.assertTrue(payload["responsibilities"])
        self.assertTrue(payload["competencies"])
        self.assertIn("Jira", payload["tools"])

    def test_job_description_generation_updates_interview_engine(self) -> None:
        response = self.client.post("/api/jd/generate-interview", json={"text": SAMPLE_JOB_DESCRIPTION})

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("profile", payload)
        self.assertIn("opening_prompt", payload)
        self.assertEqual(payload["recommended_mode"], "role_based_interview")
        self.assertIsNotNone(engine.job_description_profile)
        self.assertTrue(engine.job_description_profile["competencies"])

    def test_job_description_upload_analysis(self) -> None:
        response = self.client.post(
            "/api/jd/analyze-upload",
            files={"file": _sample_text_upload("job_description.txt", SAMPLE_JOB_DESCRIPTION)},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("raw_text", payload)
        self.assertIn("profile", payload)
        self.assertTrue(payload["profile"]["responsibilities"])

    def test_job_description_upload_generation(self) -> None:
        response = self.client.post(
            "/api/jd/generate-interview-upload",
            files={"file": _sample_text_upload("job_description.txt", SAMPLE_JOB_DESCRIPTION)},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("raw_text", payload)
        self.assertIn("profile", payload)
        self.assertIn("opening_prompt", payload)
        self.assertIsNotNone(engine.job_description_profile)

    def test_feature_plan_generation(self) -> None:
        response = self.client.post(
            "/api/features/plan",
            json={"request": "Add a delivery-risk simulation mode with competency scoring for every answer."},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["feature_type"], "interaction-driven")
        self.assertTrue(payload["generated_plan"])

    def test_voice_tts_generates_audio_file_path(self) -> None:
        response = self.client.post("/api/voice/tts", json={"text": "Tell me about a delivery tradeoff you handled."})

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("audio_file", payload)
        generated_path = Path(payload["audio_file"])
        self.assertTrue(generated_path.exists())
        self.assertGreater(generated_path.stat().st_size, 0)
        generated_path.unlink(missing_ok=True)

    def test_voice_stt_accepts_audio_upload(self) -> None:
        response = self.client.post("/api/voice/stt", files={"file": _sample_wav_upload()})

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("text", payload)
        self.assertIsInstance(payload["text"], str)


if __name__ == "__main__":
    unittest.main()
