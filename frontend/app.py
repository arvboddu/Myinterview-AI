from __future__ import annotations

import os

import requests
import streamlit as st


BACKEND = os.getenv("BACKEND_URL", "http://127.0.0.1:8001/api")
BACKEND_ROOT = BACKEND.rsplit("/api", 1)[0] if "/api" in BACKEND else BACKEND

st.set_page_config(page_title="MyInterview AI", page_icon="M", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Source+Sans+3:wght@400;600;700&display=swap');

    :root {
        --bg: #f6f1e8;
        --surface: rgba(255, 252, 247, 0.88);
        --surface-strong: #fffdf8;
        --ink: #1d2733;
        --muted: #5b6873;
        --line: rgba(29, 39, 51, 0.10);
        --accent: #b74f2c;
        --accent-2: #1f6d68;
        --shadow: 0 20px 45px rgba(54, 41, 24, 0.08);
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(183, 79, 44, 0.12), transparent 30%),
            radial-gradient(circle at top right, rgba(31, 109, 104, 0.12), transparent 28%),
            linear-gradient(180deg, #fbf7f1 0%, var(--bg) 100%);
        color: var(--ink);
        font-family: "Source Sans 3", sans-serif;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1f2c39 0%, #243847 100%);
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    [data-testid="stSidebar"] * {
        color: #f5efe5 !important;
    }

    h1, h2, h3 {
        font-family: "Space Grotesk", sans-serif !important;
        letter-spacing: -0.02em;
        color: var(--ink);
    }

    .hero-card, .content-card {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 24px;
        box-shadow: var(--shadow);
        backdrop-filter: blur(10px);
    }

    .hero-card {
        padding: 1.5rem 1.5rem 1.2rem 1.5rem;
        margin-bottom: 1rem;
    }

    .hero-kicker {
        color: var(--accent);
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 0.78rem;
    }

    .hero-title {
        font-family: "Space Grotesk", sans-serif;
        font-weight: 700;
        font-size: 2.6rem;
        line-height: 1.05;
        margin: 0.3rem 0 0.55rem 0;
    }

    .hero-copy {
        color: var(--muted);
        font-size: 1.02rem;
        line-height: 1.55;
        margin-bottom: 1rem;
    }

    .metric-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.85rem;
        margin-top: 0.75rem;
    }

    .metric-card {
        background: rgba(255,255,255,0.72);
        border: 1px solid rgba(29, 39, 51, 0.08);
        border-radius: 18px;
        padding: 0.95rem 1rem;
    }

    .metric-label {
        color: var(--muted);
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .metric-value {
        font-family: "Space Grotesk", sans-serif;
        font-size: 1.25rem;
        font-weight: 700;
        margin-top: 0.2rem;
        color: var(--ink);
    }

    .section-shell {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 22px;
        padding: 1rem 1rem 1.1rem 1rem;
        box-shadow: var(--shadow);
        margin-top: 0.6rem;
    }

    .chat-bubble {
        border-radius: 18px;
        padding: 0.95rem 1rem;
        margin-bottom: 0.75rem;
        border: 1px solid var(--line);
    }

    .chat-you {
        background: rgba(183, 79, 44, 0.10);
    }

    .chat-ai {
        background: rgba(31, 109, 104, 0.10);
    }

    .chat-speaker {
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--muted);
        margin-bottom: 0.35rem;
        font-weight: 700;
    }

    .chipline {
        display: flex;
        gap: 0.55rem;
        flex-wrap: wrap;
        margin-top: 0.7rem;
    }

    .chip {
        background: rgba(29, 39, 51, 0.06);
        border: 1px solid rgba(29, 39, 51, 0.08);
        padding: 0.45rem 0.75rem;
        border-radius: 999px;
        font-size: 0.9rem;
        color: var(--ink);
    }

    div[data-testid="stTabs"] button {
        font-family: "Space Grotesk", sans-serif;
        font-weight: 600;
    }

    .stButton > button {
        border-radius: 14px;
        border: 1px solid rgba(29, 39, 51, 0.10);
        box-shadow: none;
        font-weight: 700;
    }

    .stTextArea textarea, .stTextInput input {
        border-radius: 14px !important;
        background: rgba(255,255,255,0.72) !important;
    }

    @media (max-width: 900px) {
        .metric-grid {
            grid-template-columns: 1fr;
        }
        .hero-title {
            font-size: 2rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def initialize_state() -> None:
    defaults = {
        "messages": [],
        "resume_analysis": None,
        "resume_upload_analysis": None,
        "resume_questions": None,
        "rag_context": "",
        "voice_tts_result": None,
        "voice_stt_result": None,
        "jd_analysis": None,
        "jd_upload_analysis": None,
        "jd_interview": None,
        "feature_plan": None,
        "backend_status": None,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def probe_backend() -> None:
    health_url = f"{BACKEND_ROOT}/health"
    try:
        response = requests.get(health_url, timeout=5)
        response.raise_for_status()
        st.session_state.backend_status = response.json().get("status", "ok")
    except requests.RequestException:
        st.session_state.backend_status = "offline"


def reset_interview() -> None:
    requests.post(f"{BACKEND}/reset", timeout=20).raise_for_status()
    st.session_state.messages = []


def send_answer(message: str) -> None:
    response = requests.post(f"{BACKEND}/interview", json={"message": message}, timeout=30)
    response.raise_for_status()
    payload = response.json()
    st.session_state.messages.extend(
        [
            {"speaker": "You", "message": message},
            {"speaker": "Interview Coach", "message": payload.get("response", "")},
        ]
    )


def analyze_resume(resume_text: str) -> None:
    response = requests.post(f"{BACKEND}/resume/analyze", json={"text": resume_text}, timeout=30)
    response.raise_for_status()
    st.session_state.resume_analysis = response.json()


def upload_resume_for_analysis(file) -> None:
    response = requests.post(
        f"{BACKEND}/resume/upload",
        files={"file": (file.name, file.getvalue(), file.type or "application/octet-stream")},
        timeout=60,
    )
    response.raise_for_status()
    st.session_state.resume_upload_analysis = response.json()


def generate_resume_questions(file) -> None:
    response = requests.post(
        f"{BACKEND}/resume/questions",
        files={"file": (file.name, file.getvalue(), file.type or "application/octet-stream")},
        timeout=60,
    )
    response.raise_for_status()
    st.session_state.resume_questions = response.json()


def search_rag(query: str) -> None:
    response = requests.get(f"{BACKEND}/rag/search", params={"q": query}, timeout=30)
    response.raise_for_status()
    st.session_state.rag_context = response.json().get("context", "")


def synthesize_voice(text: str) -> None:
    response = requests.post(f"{BACKEND}/voice/tts", json={"text": text}, timeout=30)
    response.raise_for_status()
    st.session_state.voice_tts_result = response.json()


def transcribe_voice(file) -> None:
    response = requests.post(
        f"{BACKEND}/voice/stt",
        files={"file": (file.name, file.getvalue(), file.type or "application/octet-stream")},
        timeout=60,
    )
    response.raise_for_status()
    st.session_state.voice_stt_result = response.json()


def analyze_jd(text: str) -> None:
    response = requests.post(f"{BACKEND}/jd/analyze", json={"text": text}, timeout=60)
    response.raise_for_status()
    st.session_state.jd_analysis = response.json()


def analyze_jd_upload(file) -> None:
    response = requests.post(
        f"{BACKEND}/jd/analyze-upload",
        files={"file": (file.name, file.getvalue(), file.type or "application/octet-stream")},
        timeout=60,
    )
    response.raise_for_status()
    st.session_state.jd_upload_analysis = response.json()


def generate_jd_interview(text: str) -> None:
    response = requests.post(f"{BACKEND}/jd/generate-interview", json={"text": text}, timeout=60)
    response.raise_for_status()
    payload = response.json()
    st.session_state.jd_interview = payload
    opening_prompt = payload.get("opening_prompt", "")
    if opening_prompt:
        st.session_state.messages = [{"speaker": "System", "message": opening_prompt}]


def generate_jd_interview_upload(file) -> None:
    response = requests.post(
        f"{BACKEND}/jd/generate-interview-upload",
        files={"file": (file.name, file.getvalue(), file.type or "application/octet-stream")},
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    st.session_state.jd_interview = payload
    opening_prompt = payload.get("opening_prompt", "")
    if opening_prompt:
        st.session_state.messages = [{"speaker": "System", "message": opening_prompt}]


def plan_feature(request_text: str) -> None:
    response = requests.post(f"{BACKEND}/features/plan", json={"request": request_text}, timeout=30)
    response.raise_for_status()
    st.session_state.feature_plan = response.json()


def render_list_block(title: str, items: list[str]) -> None:
    if not items:
        return
    st.markdown(f"**{title}**")
    for item in items:
        st.write(f"- {item}")


def render_question_groups(payload: dict) -> None:
    categories = [
        ("Behavioral", "behavioral_questions"),
        ("Delivery", "delivery_questions"),
        ("Leadership", "leadership_questions"),
        ("Execution", "execution_questions"),
        ("Risk Mitigation", "risk_mitigation_questions"),
        ("Follow Up", "follow_up_questions"),
    ]
    for label, key in categories:
        items = payload.get(key, [])
        if items:
            st.markdown(f"**{label} Questions**")
            for item in items:
                st.write(f"- {item}")


initialize_state()
probe_backend()

st.markdown(
    """
    <div class="hero-card">
        <div class="hero-kicker">Interview Prep Workspace</div>
        <div class="hero-title">MyInterview AI</div>
        <div class="hero-copy">
            Practice role-specific interviews, break down resumes and job descriptions,
            and shape new coaching workflows from a single workspace.
        </div>
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">Core Modes</div>
                <div class="metric-value">Interview, JD, Resume</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Extension Paths</div>
                <div class="metric-value">Option A, B, C</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Active Stack</div>
                <div class="metric-value">FastAPI + Streamlit</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if st.session_state.get("backend_status") != "ok":
    st.warning("Backend is not reachable right now. Start the backend service before using the workspace.")
else:
    st.success("Backend connected. MyInterview AI is ready.")

with st.sidebar:
    st.markdown("## MyInterview AI")
    st.write("A local workspace for interview practice, role intelligence, and feature design.")
    st.markdown("---")
    st.subheader("Session")
    st.write("The interview coach keeps a rolling context until you reset it.")
    if st.button("Reset Interview", use_container_width=True):
        try:
            reset_interview()
        except requests.RequestException as exc:
            st.error(f"Could not reset interview: {exc}")

    st.markdown("---")
    st.subheader("What You Can Do")
    st.write("- Run a guided interview conversation")
    st.write("- Analyze a job description or uploaded JD file")
    st.write("- Turn feature ideas into implementation plans")
    st.write("- Review resumes, search context, and test voice routes")

tabs = st.tabs(
    [
        "Interview Studio",
        "JD Intelligence",
        "Feature Lab",
        "Resume Review",
        "RAG Search",
        "Voice Tools",
    ]
)
tab1, tab2, tab3, tab4, tab5, tab6 = tabs

with tab1:
    st.markdown('<div class="section-shell">', unsafe_allow_html=True)
    st.subheader("Interview Studio")
    st.caption("Use this area to simulate a live coaching thread. JD-based mode can pre-load the conversation from the JD tab.")
    if not st.session_state.messages:
        st.info("Start by asking for an interview question, or generate JD-based mode in the next tab.")

    for item in st.session_state.messages:
        speaker = item["speaker"]
        bubble_class = "chat-you" if speaker == "You" else "chat-ai"
        st.markdown(
            f"""
            <div class="chat-bubble {bubble_class}">
                <div class="chat-speaker">{speaker}</div>
                <div>{item['message']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    answer = st.text_area(
        "Interview message",
        height=180,
        placeholder="Example: Ask me a PM-delivery interview question about stakeholder management.",
    )
    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("Send to Coach", type="primary", use_container_width=True):
            if not answer.strip():
                st.warning("Write a message before sending.")
            else:
                try:
                    send_answer(answer)
                    st.rerun()
                except requests.RequestException as exc:
                    st.error(f"Could not send message: {exc}")
    with col2:
        if st.button("Clear Transcript", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-shell">', unsafe_allow_html=True)
    st.subheader("Job Description Intelligence")
    st.caption("Drive Option A and Option C from pasted text or uploaded files.")
    jd_text = st.text_area(
        "Paste job description",
        height=240,
        placeholder="Paste the full JD here to extract responsibilities, competencies, KPIs, and interview scenarios.",
    )
    jd_file = st.file_uploader("Upload JD file", type=["pdf", "docx", "txt"], key="jd_upload")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Analyze Text JD", use_container_width=True):
            if not jd_text.strip():
                st.warning("Paste a job description first.")
            else:
                try:
                    analyze_jd(jd_text)
                except requests.RequestException as exc:
                    st.error(f"Could not analyze JD: {exc}")
    with col2:
        if st.button("Start From Text", use_container_width=True):
            if not jd_text.strip():
                st.warning("Paste a job description first.")
            else:
                try:
                    generate_jd_interview(jd_text)
                except requests.RequestException as exc:
                    st.error(f"Could not generate JD-based interview: {exc}")
    with col3:
        if st.button("Analyze JD File", use_container_width=True):
            if jd_file is None:
                st.warning("Upload a JD file first.")
            else:
                try:
                    analyze_jd_upload(jd_file)
                except requests.RequestException as exc:
                    st.error(f"Could not analyze uploaded JD: {exc}")
    with col4:
        if st.button("Start From File", use_container_width=True):
            if jd_file is None:
                st.warning("Upload a JD file first.")
            else:
                try:
                    generate_jd_interview_upload(jd_file)
                except requests.RequestException as exc:
                    st.error(f"Could not generate JD-based interview from file: {exc}")

    jd_analysis = st.session_state.get("jd_analysis")
    if jd_analysis:
        st.markdown("### JD Analysis From Pasted Text")
        st.write(jd_analysis.get("summary", ""))
        render_list_block("Responsibilities", jd_analysis.get("responsibilities", []))
        render_list_block("Requirements", jd_analysis.get("requirements", []))
        render_list_block("Competencies", jd_analysis.get("competencies", []))
        render_list_block("KPIs", jd_analysis.get("kpis", []))
        render_list_block("Tools", jd_analysis.get("tools", []))
        if jd_analysis.get("skill_matrix"):
            st.markdown("**Skill Matrix**")
            st.json(jd_analysis["skill_matrix"])

    jd_upload_analysis = st.session_state.get("jd_upload_analysis")
    if jd_upload_analysis:
        profile = jd_upload_analysis.get("profile", {})
        st.markdown("### JD Analysis From Uploaded File")
        st.write(profile.get("summary", ""))
        with st.expander("Extracted JD Text"):
            st.write(jd_upload_analysis.get("raw_text", ""))
        render_list_block("Responsibilities", profile.get("responsibilities", []))
        render_list_block("Requirements", profile.get("requirements", []))
        render_list_block("Competencies", profile.get("competencies", []))
        render_list_block("KPIs", profile.get("kpis", []))
        render_list_block("Tools", profile.get("tools", []))

    jd_interview = st.session_state.get("jd_interview")
    if jd_interview:
        st.markdown("### Generated Interview Package")
        st.write(jd_interview.get("opening_prompt", ""))
        profile = jd_interview.get("profile", {})
        categories = profile.get("question_categories", {})
        if categories:
            st.markdown('<div class="chipline">' + "".join([f'<div class="chip">{key.replace("_", " ").title()}</div>' for key in categories.keys()]) + "</div>", unsafe_allow_html=True)
            st.json(categories)
    st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-shell">', unsafe_allow_html=True)
    st.subheader("Feature Lab")
    st.caption("Describe new functionality in plain language and turn it into a concrete implementation plan.")
    feature_request = st.text_area(
        "Describe a feature to add",
        height=180,
        placeholder="Example: Add competency scoring for every answer with a delivery-risk simulation mode.",
    )
    if st.button("Generate Feature Plan", use_container_width=True):
        if not feature_request.strip():
            st.warning("Describe the feature first.")
        else:
            try:
                plan_feature(feature_request)
            except requests.RequestException as exc:
                st.error(f"Could not plan feature: {exc}")

    feature_plan_result = st.session_state.get("feature_plan")
    if feature_plan_result:
        st.markdown("### Planned Extension")
        st.json(feature_plan_result)
    st.markdown("</div>", unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="section-shell">', unsafe_allow_html=True)
    st.subheader("Resume Review")
    st.caption("Analyze pasted resume content, inspect uploaded resume text, and generate interview questions from files.")
    resume_text = st.text_area(
        "Paste resume text",
        height=220,
        placeholder="Paste the resume content here to get backend analysis output.",
    )
    uploaded_file = st.file_uploader("Upload resume file", type=["pdf", "docx", "txt"])
    col1, col2, col3 = st.columns(3)
    with col1:
        analyze_clicked = st.button("Analyze Text Resume", use_container_width=True)
    with col2:
        upload_clicked = st.button("Analyze Uploaded Resume", use_container_width=True)
    with col3:
        question_clicked = st.button("Generate Questions", use_container_width=True)

    if analyze_clicked:
        if not resume_text.strip():
            st.warning("Paste some resume content first.")
        else:
            try:
                analyze_resume(resume_text)
            except requests.RequestException as exc:
                st.error(f"Could not analyze resume: {exc}")

    if upload_clicked:
        if uploaded_file is None:
            st.warning("Upload a resume file first.")
        else:
            try:
                upload_resume_for_analysis(uploaded_file)
            except requests.RequestException as exc:
                st.error(f"Could not analyze uploaded resume: {exc}")

    if question_clicked:
        if uploaded_file is None:
            st.warning("Upload a resume file first.")
        else:
            try:
                generate_resume_questions(uploaded_file)
            except requests.RequestException as exc:
                st.error(f"Could not generate questions: {exc}")

    result = st.session_state.get("resume_analysis")
    if result:
        st.markdown("### Analysis From Pasted Text")
        st.write(result.get("analysis", ""))

    uploaded_result = st.session_state.get("resume_upload_analysis")
    if uploaded_result:
        st.markdown("### Analysis From Uploaded File")
        st.write(uploaded_result.get("analysis", ""))
        with st.expander("Extracted Resume Text"):
            st.write(uploaded_result.get("raw_text", ""))

    generated = st.session_state.get("resume_questions")
    if generated:
        st.markdown("### Generated Questions")
        question_payload = generated.get("questions", generated)
        if isinstance(question_payload, dict):
            render_question_groups(question_payload)
            if question_payload.get("notes"):
                st.caption(question_payload["notes"])
        else:
            st.json(question_payload)
    st.markdown("</div>", unsafe_allow_html=True)

with tab5:
    st.markdown('<div class="section-shell">', unsafe_allow_html=True)
    st.subheader("RAG Search")
    st.caption("Inspect the context that the retrieval layer sends into interviews and analysis flows.")
    query = st.text_input("Search query", placeholder="stakeholder management delivery metrics")
    if st.button("Search Context", use_container_width=True):
        if not query.strip():
            st.warning("Enter a search query first.")
        else:
            try:
                search_rag(query)
            except requests.RequestException as exc:
                st.error(f"Could not search context: {exc}")

    if st.session_state.get("rag_context"):
        st.markdown("### Retrieved Context")
        st.code(st.session_state.rag_context)
    else:
        st.caption("No context retrieved yet. Try a broader search like 'delivery risk' or 'stakeholder management'.")
    st.markdown("</div>", unsafe_allow_html=True)

with tab6:
    st.markdown('<div class="section-shell">', unsafe_allow_html=True)
    st.subheader("Voice Tools")
    st.caption("Exercise the current placeholder speech-to-text and text-to-speech flows from the same workspace.")
    tts_text = st.text_area(
        "Text for text-to-speech",
        height=120,
        placeholder="Tell me about a delivery tradeoff you handled.",
    )
    stt_file = st.file_uploader("Upload audio for speech-to-text", type=["wav", "mp3", "m4a"], key="voice_upload")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Run TTS", use_container_width=True):
            if not tts_text.strip():
                st.warning("Enter text before calling TTS.")
            else:
                try:
                    synthesize_voice(tts_text)
                except requests.RequestException as exc:
                    st.error(f"Could not synthesize speech: {exc}")
    with col2:
        if st.button("Run STT", use_container_width=True):
            if stt_file is None:
                st.warning("Upload an audio file first.")
            else:
                try:
                    transcribe_voice(stt_file)
                except requests.RequestException as exc:
                    st.error(f"Could not transcribe audio: {exc}")

    tts_result = st.session_state.get("voice_tts_result")
    if tts_result:
        st.markdown("### TTS Result")
        audio_file = tts_result.get("audio_file", "")
        if audio_file:
            st.audio(f"{BACKEND_ROOT}/{audio_file.replace(chr(92), '/')}")
            st.caption(audio_file)

    stt_result = st.session_state.get("voice_stt_result")
    if stt_result:
        st.markdown("### STT Result")
        st.write(stt_result.get("text", ""))
    st.markdown("</div>", unsafe_allow_html=True)
