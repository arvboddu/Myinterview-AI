from __future__ import annotations

import os
import time
from datetime import datetime

import requests
import streamlit as st

BACKEND = os.getenv("BACKEND_URL", "http://localhost:8001/api")
BACKEND_ROOT = os.getenv("BACKEND_ROOT", "http://localhost:8001")
V1_BACKEND = os.getenv("V1_BACKEND", f"{BACKEND_ROOT}/v1")
GATEWAY_BACKEND = os.getenv("GATEWAY_BACKEND", f"{BACKEND_ROOT}/v1/gateway")

st.set_page_config(
    page_title="MyInterview AI - AI-Powered Interview Copilot",
    page_icon="M",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

:root {
    --bg-primary: #ffffff;
    --bg-secondary: #f8fafc;
    --bg-tertiary: #f1f5f9;
    --bg-card: #ffffff;
    --bg-elevated: #ffffff;
    --accent-primary: #6366f1;
    --accent-primary-light: #818cf8;
    --accent-secondary: #8b5cf6;
    --accent-success: #10b981;
    --accent-success-light: #34d399;
    --accent-warning: #f59e0b;
    --accent-danger: #ef4444;
    --accent-cyan: #06b6d4;
    --accent-pink: #ec4899;
    --accent-blue: #3b82f6;
    --accent-orange: #f97316;
    --text-primary: #0f172a;
    --text-secondary: #475569;
    --text-muted: #94a3b8;
    --text-light: #cbd5e1;
    --border-color: #e2e8f0;
    --border-light: #f1f5f9;
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    --shadow-glow: 0 0 40px rgba(99, 102, 241, 0.15);
    --gradient-primary: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    --gradient-success: linear-gradient(135deg, #10b981 0%, #06b6d4 100%);
    --gradient-warm: linear-gradient(135deg, #f59e0b 0%, #f97316 100%);
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-xl: 24px;
    --radius-full: 9999px;
}

* { 
    font-family: 'Inter', 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important; 
    box-sizing: border-box;
}

html, body {
    background: var(--bg-secondary) !important;
    color: var(--text-primary) !important;
    min-height: 100vh;
    scroll-behavior: smooth;
}

/* Expander Styles */
[data-testid="stExpander"] {
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-md) !important;
    background: var(--bg-card) !important;
}

[data-testid="stExpander"] div:first-child {
    font-weight: 600 !important;
}

.stDeployer { display: none !important; }

/* Fix expander arrow icon */
[ data-testid="stExpander"] svg {
    width: 1rem !important;
    height: 1rem !important;
}

.stApp { background: transparent !important; }

/* Custom Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-tertiary); }
::-webkit-scrollbar-thumb { background: var(--accent-primary-light); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent-primary); }

/* Sidebar - Ensure it's always on top and interactive */
[data-testid="stSidebar"] {
    background: var(--bg-card) !important;
    border-right: 1px solid var(--border-color);
    box-shadow: var(--shadow-md);
    z-index: 999999 !important;
    position: relative !important;
    overflow: visible !important;
}

[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: var(--text-primary) !important;
}

/* CRITICAL: Ensure ALL sidebar elements are clickable */
[data-testid="stSidebar"] *,
[data-testid="stSidebar"] *::before,
[data-testid="stSidebar"] *::after {
    pointer-events: auto !important;
}

/* Selectbox dropdown - ensure it's above everything */
[data-testid="stSidebar"] [data-baseweb="select"],
[data-testid="stSidebar"] [data-baseweb="popover"],
[data-testid="stSidebar"] [data-baseweb="menu"] {
    pointer-events: auto !important;
    z-index: 9999999 !important;
}

/* Dropdown menu items */
[data-testid="stSidebar"] [role="option"],
[data-testid="stSidebar"] [role="listbox"] {
    pointer-events: auto !important;
}

/* Override any overlay blocking */
[data-testid="stSidebar"] .stSelectbox,
[data-testid="stSidebar"] [data-testid="stSelectbox"] {
    position: relative;
    z-index: 1;
}

/* Checkbox styling */
[data-testid="stSidebar"] .stCheckbox {
    pointer-events: auto !important;
}

/* Button styling */
[data-testid="stSidebar"] .stButton {
    pointer-events: auto !important;
}

/* Text area styling */
[data-testid="stSidebar"] .stTextArea {
    pointer-events: auto !important;
}

/* Multiselect styling */
[data-testid="stSidebar"] [data-baseweb="tag"] {
    pointer-events: auto !important;
}

/* Main content should NOT block sidebar */
[data-testid="stMainBlockContainer"] {
    pointer-events: none !important;
}

[data-testid="stMainBlockContainer"] * {
    pointer-events: auto !important;
}

/* Headers */
h1, h2, h3, h4, h5, h6 {
    color: var(--text-primary) !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em;
}

/* Hero Section */
.hero-section {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 50%, #f1f5f9 100%);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-xl);
    padding: 48px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-lg);
}

.hero-section::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(99, 102, 241, 0.08) 0%, transparent 70%);
    pointer-events: none;
}

.hero-section::after {
    content: '';
    position: absolute;
    bottom: -30%;
    left: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(16, 185, 129, 0.06) 0%, transparent 70%);
    pointer-events: none;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(99, 102, 241, 0.1);
    border: 1px solid rgba(99, 102, 241, 0.2);
    padding: 8px 16px;
    border-radius: var(--radius-full);
    font-size: 0.75rem;
    color: var(--accent-primary);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 16px;
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 800;
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 16px 0;
    line-height: 1.1;
}

.hero-subtitle {
    font-size: 1.2rem;
    color: var(--text-secondary);
    line-height: 1.7;
    max-width: 650px;
    margin: 0;
}

/* Stats Grid */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 20px;
    margin-top: 40px;
    position: relative;
    z-index: 1;
}

.stat-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 24px;
    text-align: center;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: var(--shadow-sm);
}

.stat-card:hover {
    transform: translateY(-6px);
    box-shadow: var(--shadow-xl);
    border-color: var(--accent-primary-light);
}

.stat-icon { font-size: 2.5rem; margin-bottom: 12px; }
.stat-value { font-size: 2rem; font-weight: 800; color: var(--accent-primary); }
.stat-label { font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.08em; margin-top: 8px; font-weight: 500; }

/* Content Card */
.content-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-xl);
    padding: 28px;
    margin-bottom: 24px;
    box-shadow: var(--shadow-md);
    transition: all 0.3s ease;
}

.content-card:hover {
    box-shadow: var(--shadow-lg);
    border-color: var(--accent-primary-light);
}

/* Section Shell */
.section-shell {
    background: var(--bg-card);
    border-radius: var(--radius-xl);
    padding: 32px;
    border: 1px solid var(--border-color);
    box-shadow: var(--shadow-md);
}

/* Phase Indicator */
.phase-indicator {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 16px 24px;
    background: var(--bg-card);
    border-radius: var(--radius-lg);
    margin-bottom: 28px;
    border: 1px solid var(--border-color);
    box-shadow: var(--shadow-sm);
}

.phase-step {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 20px;
    border-radius: var(--radius-md);
    background: var(--bg-tertiary);
    border: 1px solid var(--border-color);
    color: var(--text-muted);
    font-weight: 500;
    font-size: 0.9rem;
    transition: all 0.3s ease;
}

.phase-step.active {
    background: var(--gradient-primary);
    border-color: transparent;
    color: white;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.phase-step.completed {
    background: rgba(16, 185, 129, 0.1);
    border-color: rgba(16, 185, 129, 0.3);
    color: var(--accent-success);
}

.phase-connector {
    width: 40px;
    height: 2px;
    background: linear-gradient(90deg, var(--border-color), var(--accent-primary-light));
    border-radius: 1px;
}

/* Chat Bubbles */
.chat-container {
    max-height: 450px;
    overflow-y: auto;
    padding: 20px;
    background: var(--bg-secondary);
    border-radius: var(--radius-lg);
    margin-bottom: 20px;
    border: 1px solid var(--border-light);
}

.chat-bubble {
    border-radius: var(--radius-lg);
    padding: 20px;
    margin-bottom: 16px;
    font-size: 0.95rem;
    line-height: 1.7;
    position: relative;
    animation: fadeIn 0.3s ease;
    box-shadow: var(--shadow-sm);
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}

.chat-you {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(139, 92, 246, 0.05) 100%);
    border: 1px solid rgba(99, 102, 241, 0.15);
    border-left: 4px solid var(--accent-primary);
    margin-left: 24px;
}

.chat-ai {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(6, 182, 212, 0.05) 100%);
    border: 1px solid rgba(16, 185, 129, 0.15);
    border-left: 4px solid var(--accent-success);
    margin-right: 24px;
}

.chat-system {
    background: rgba(245, 158, 11, 0.08);
    border: 1px solid rgba(245, 158, 11, 0.15);
    border-left: 4px solid var(--accent-warning);
    margin-right: 24px;
    font-style: italic;
}

.chat-speaker {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-muted);
    margin-bottom: 8px;
    font-weight: 600;
}

/* Stealth Panel */
.stealth-panel {
    position: fixed;
    bottom: 24px;
    right: 24px;
    width: 380px;
    background: var(--bg-card);
    border: 2px solid var(--accent-primary);
    border-radius: var(--radius-xl);
    padding: 24px;
    box-shadow: 0 25px 50px -12px rgba(99, 102, 241, 0.25);
    z-index: 1000;
    display: none;
}

.stealth-panel.visible { display: block; }

.stealth-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border-color);
}

.stealth-title {
    font-size: 1rem;
    font-weight: 700;
    color: var(--accent-primary);
    display: flex;
    align-items: center;
    gap: 8px;
}

.stealth-close {
    background: var(--bg-tertiary);
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    font-size: 1.2rem;
    width: 32px;
    height: 32px;
    border-radius: var(--radius-sm);
    transition: all 0.2s;
}

.stealth-close:hover { background: var(--accent-danger); color: white; }

/* Difficulty Badge */
.difficulty-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 16px;
    border-radius: var(--radius-full);
    font-size: 0.8rem;
    font-weight: 600;
}

.difficulty-easy { background: rgba(16, 185, 129, 0.1); color: var(--accent-success); border: 1px solid rgba(16, 185, 129, 0.2); }
.difficulty-medium { background: rgba(245, 158, 11, 0.1); color: var(--accent-warning); border: 1px solid rgba(245, 158, 11, 0.2); }
.difficulty-hard { background: rgba(239, 68, 68, 0.1); color: var(--accent-danger); border: 1px solid rgba(239, 68, 68, 0.2); }

/* Progress Ring */
.progress-ring-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
}

.progress-ring {
    width: 140px;
    height: 140px;
    border-radius: 50%;
    background: conic-gradient(var(--accent-primary) 0%, var(--bg-tertiary) 0%);
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    box-shadow: var(--shadow-md);
}

.progress-ring::before {
    content: '';
    position: absolute;
    width: 110px;
    height: 110px;
    border-radius: 50%;
    background: var(--bg-card);
}

.progress-value {
    position: relative;
    font-size: 2rem;
    font-weight: 800;
    color: var(--accent-primary);
}

/* Tabs */
.stTabs [data-testid="stTabBar"] {
    background: var(--bg-card);
    border-radius: var(--radius-lg);
    padding: 6px;
    border: 1px solid var(--border-color);
    box-shadow: var(--shadow-sm);
    margin-bottom: 24px;
}

.stTabs button {
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    border-radius: var(--radius-md) !important;
    padding: 12px 20px !important;
    transition: all 0.2s ease !important;
    font-size: 0.9rem;
}

.stTabs button:hover { 
    color: var(--accent-primary) !important; 
    background: rgba(99, 102, 241, 0.08) !important; 
}

.stTabs button[aria-selected="true"] {
    color: white !important;
    background: var(--gradient-primary) !important;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
}

/* Buttons */
.stButton > button {
    border-radius: var(--radius-md) !important;
    border: none !important;
    background: var(--gradient-primary) !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 12px 24px !important;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.25) !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    font-size: 0.9rem;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(99, 102, 241, 0.35) !important;
}

.stButton > button:active {
    transform: translateY(0);
}

/* Inputs */
.stTextArea textarea, .stTextInput input, .stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    padding: 14px 16px !important;
    font-size: 0.95rem !important;
    transition: all 0.2s !important;
}

.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: var(--accent-primary) !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-lg) !important;
    padding: 20px !important;
    box-shadow: var(--shadow-sm);
}

[data-testid="stMetricValue"] { 
    color: var(--accent-primary) !important; 
    font-weight: 700 !important; 
    font-size: 1.5rem !important;
}

[data-testid="stMetricLabel"] { 
    color: var(--text-muted) !important; 
    font-weight: 500 !important; 
}

/* File Uploader */
.stFileUploader [data-testid="stFileUploadDropzone"] {
    background: var(--bg-secondary) !important;
    border: 2px dashed var(--border-color) !important;
    border-radius: var(--radius-lg) !important;
    padding: 40px !important;
    transition: all 0.2s !important;
}

.stFileUploader [data-testid="stFileUploadDropzone"]:hover {
    border-color: var(--accent-primary) !important;
    background: rgba(99, 102, 241, 0.05) !important;
}

/* Expanders */
.streamlit-expanderHeader {
    background: var(--bg-secondary) !important;
    border-radius: var(--radius-md) !important;
    border: 1px solid var(--border-color) !important;
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}

.streamlit-expanderContent {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-top: none !important;
    border-radius: 0 0 var(--radius-md) var(--radius-md) !important;
}

/* Success/Warning/Info boxes */
.stAlert {
    border-radius: var(--radius-md) !important;
    border: none !important;
}

/* Roadmap Cards */
.roadmap-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 24px;
    margin: 16px 0;
    display: flex;
    align-items: center;
    gap: 20px;
    transition: all 0.3s ease;
    box-shadow: var(--shadow-sm);
}

.roadmap-card:hover {
    border-color: var(--accent-primary-light);
    box-shadow: var(--shadow-lg);
    transform: translateX(4px);
}

.roadmap-week {
    background: var(--gradient-primary);
    color: white;
    padding: 16px 20px;
    border-radius: var(--radius-md);
    font-weight: 700;
    font-size: 0.9rem;
    min-width: 100px;
    text-align: center;
}

.roadmap-content h4 {
    margin: 0 0 4px 0;
    color: var(--accent-primary);
    font-weight: 600;
}

.roadmap-content p {
    margin: 0;
    color: var(--text-secondary);
    font-size: 0.9rem;
}

/* Feature Cards */
.feature-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 24px;
    transition: all 0.3s ease;
    text-align: center;
}

.feature-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
    border-color: var(--accent-primary-light);
}

.feature-icon { font-size: 3rem; margin-bottom: 16px; }
.feature-title { font-weight: 700; color: var(--text-primary); margin-bottom: 8px; }
.feature-desc { color: var(--text-secondary); font-size: 0.9rem; }

/* Info Box */
.info-box {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(139, 92, 246, 0.05) 100%);
    border: 1px solid rgba(99, 102, 241, 0.15);
    border-radius: var(--radius-lg);
    padding: 24px;
    margin: 16px 0;
}

/* Divider */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border-color), transparent);
    margin: 32px 0;
}

/* Responsive */
@media (max-width: 1200px) { .stats-grid { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 768px) { 
    .stats-grid { grid-template-columns: repeat(2, 1fr); } 
    .hero-title { font-size: 2.5rem; }
    .phase-indicator { flex-wrap: wrap; }
    .stealth-panel { width: calc(100% - 48px); }
}
</style>
""",
    unsafe_allow_html=True,
)


def initialize_state() -> None:
    defaults = {
        "messages": [],
        "copilot_session_id": None,
        "copilot_transcript": [],
        "copilot_feedback": None,
        "coding_question": None,
        "coding_result": None,
        "coding_review": None,
        "system_design_prompt": None,
        "system_design_review": None,
        "resume_analysis": None,
        "resume_upload_analysis": None,
        "resume_questions": None,
        "rag_context": "",
        "voice_tts_result": None,
        "voice_stt_result": None,
        "jd_analysis": None,
        "jd_upload_analysis": None,
        "jd_interview": None,
        "ai_jd_questions": None,
        "feature_plan": None,
        "backend_status": None,
        "salary_result": None,
        "salary_benchmarks": None,
        "resume_builder_result": None,
        "career_coach_response": None,
        "career_path": None,
        "phone_session_id": None,
        "phone_transcript": [],
        "phone_scores": None,
        "analytics_result": None,
        "user_profile": None,
        "prep_plan": None,
        "stealth_mode": False,
        "stealth_visible": False,
        "stealth_suggestions": [],
        "current_phase": 1,
        "difficulty_level": "medium",
        "interview_session_id": None,
        "performance_history": [],
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
    st.session_state.current_phase = 1


def send_answer(message: str) -> None:
    response = requests.post(
        f"{BACKEND}/interview", json={"message": message}, timeout=10
    )
    response.raise_for_status()
    payload = response.json()
    st.session_state.messages.extend(
        [
            {"speaker": "You", "message": message},
            {"speaker": "Interview Coach", "message": payload.get("response", "")},
        ]
    )
    if st.session_state.stealth_mode:
        generate_stealth_hint(payload.get("response", ""))


def start_live_copilot(role: str, focus: str) -> None:
    response = requests.post(
        f"{BACKEND}/copilot/start", json={"role": role, "focus": focus}, timeout=10
    )
    response.raise_for_status()
    payload = response.json()
    st.session_state.copilot_session_id = payload.get("session_id")
    st.session_state.copilot_transcript = [
        {"speaker": "Copilot", "message": payload.get("opening_prompt", "")}
    ]
    st.session_state.copilot_feedback = None


def send_copilot_answer(message: str) -> None:
    response = requests.post(
        f"{BACKEND}/copilot/ask",
        json={"session_id": st.session_state.copilot_session_id, "message": message},
        timeout=10,
    )
    response.raise_for_status()
    payload = response.json()
    st.session_state.copilot_transcript.extend(
        [
            {"speaker": "You", "message": message},
            {"speaker": "Copilot", "message": payload.get("response", "")},
        ]
    )
    st.session_state.copilot_feedback = {
        "coaching_note": payload.get("coaching_note", ""),
        "difficulty": payload.get("difficulty", "medium"),
    }


def review_copilot_answer(answer: str) -> None:
    response = requests.post(
        f"{BACKEND}/copilot/feedback",
        json={"session_id": st.session_state.copilot_session_id, "answer": answer},
        timeout=10,
    )
    response.raise_for_status()
    st.session_state.copilot_feedback = response.json()


def reset_live_copilot() -> None:
    if not st.session_state.copilot_session_id:
        st.session_state.copilot_transcript = []
        st.session_state.copilot_feedback = None
        return
    response = requests.post(
        f"{BACKEND}/copilot/reset",
        json={"session_id": st.session_state.copilot_session_id},
        timeout=10,
    )
    response.raise_for_status()
    st.session_state.copilot_session_id = None
    st.session_state.copilot_transcript = []
    st.session_state.copilot_feedback = None


def analyze_resume(resume_text: str) -> None:
    response = requests.post(
        f"{BACKEND}/resume/analyze", json={"text": resume_text}, timeout=10
    )
    response.raise_for_status()
    st.session_state.resume_analysis = response.json()


def upload_resume_for_analysis(file) -> None:
    response = requests.post(
        f"{V1_BACKEND}/resume/upload",
        files={
            "file": (
                file.name,
                file.getvalue(),
                file.type or "application/octet-stream",
            )
        },
        timeout=15,
    )
    response.raise_for_status()
    st.session_state.resume_upload_analysis = response.json()


def generate_resume_questions(file) -> None:
    response = requests.post(
        f"{BACKEND}/resume/questions",
        files={
            "file": (
                file.name,
                file.getvalue(),
                file.type or "application/octet-stream",
            )
        },
        timeout=15,
    )
    response.raise_for_status()
    st.session_state.resume_questions = response.json()


def search_rag(query: str) -> None:
    response = requests.get(f"{BACKEND}/rag/search", params={"q": query}, timeout=10)
    response.raise_for_status()
    st.session_state.rag_context = response.json().get("context", "")


def synthesize_voice(text: str) -> None:
    response = requests.post(f"{BACKEND}/voice/tts", json={"text": text}, timeout=10)
    response.raise_for_status()
    st.session_state.voice_tts_result = response.json()


def transcribe_voice(file) -> None:
    response = requests.post(
        f"{BACKEND}/voice/stt",
        files={
            "file": (
                file.name,
                file.getvalue(),
                file.type or "application/octet-stream",
            )
        },
        timeout=15,
    )
    response.raise_for_status()
    st.session_state.voice_stt_result = response.json()


def analyze_jd(text: str) -> None:
    response = requests.post(f"{BACKEND}/jd/analyze", json={"text": text}, timeout=15)
    response.raise_for_status()
    st.session_state.jd_analysis = response.json()


def generate_ai_jd_questions(text: str) -> None:
    response = requests.post(
        f"{BACKEND}/jd/generate-ai-questions", json={"text": text}, timeout=15
    )
    response.raise_for_status()
    st.session_state.ai_jd_questions = response.json()


def generate_copilot_answer(
    question: str,
    role: str = "Professional",
    context: str = "",
    competencies: list = None,
) -> dict:
    payload = {
        "question": question,
        "role": role,
        "context": context,
        "competencies": competencies or [],
        "difficulty": "medium",
    }
    response = requests.post(
        f"{BACKEND}/copilot/generate-answer", json=payload, timeout=180
    )
    response.raise_for_status()
    return response.json()


def generate_enhanced_answer(
    question: str,
    resume_context: dict = None,
    role_context: dict = None,
    materials: list = None,
    tone: str = "professional",
    length: str = "paragraph",
    thinking_mode: bool = False,
) -> dict:
    payload = {
        "question": question,
        "resume_context": resume_context or {},
        "role_context": role_context or {},
        "materials": materials or [],
        "tone": tone,
        "length": length,
        "thinking_mode": thinking_mode,
    }
    response = requests.post(
        f"{BACKEND}/interview/answer/generate", json=payload, timeout=60
    )
    response.raise_for_status()
    return response.json()


def format_answer(
    answer: str, length: str = "paragraph", tone: str = "professional"
) -> dict:
    payload = {
        "answer": answer,
        "length": length,
        "tone": tone,
    }
    response = requests.post(
        f"{BACKEND}/interview/answer/format", json=payload, timeout=10
    )
    response.raise_for_status()
    return response.json()


def generate_full_interview_answer(
    question: str,
    resume_context: dict = None,
    job_description: str = None,
    role: str = "Professional",
    language: str = "en",
    model: str = "advanced",
    category: str = "behavioral",
    thinking_mode: bool = False,
    answer_length: str = "paragraph",
    tone: str = "professional",
    materials: list = None,
) -> dict:
    payload = {
        "question": question,
        "resume_context": resume_context or {},
        "job_description": job_description,
        "role": role,
        "language": language,
        "model": model,
        "category": category,
        "thinking_mode": thinking_mode,
        "answer_length": answer_length,
        "tone": tone,
        "materials": materials or [],
    }
    response = requests.post(
        f"{BACKEND}/interview/full-interview", json=payload, timeout=60
    )
    response.raise_for_status()
    return response.json()


def generate_jd_interview(text: str) -> None:
    response = requests.post(
        f"{BACKEND}/jd/generate-interview", json={"text": text}, timeout=15
    )
    response.raise_for_status()
    payload = response.json()
    st.session_state.jd_interview = payload
    opening_prompt = payload.get("opening_prompt", "")
    if opening_prompt:
        st.session_state.messages = [{"speaker": "System", "message": opening_prompt}]


def generate_coding_question(language: str, topic: str, difficulty: str) -> None:
    response = requests.post(
        f"{BACKEND}/coding/generate-question",
        json={"language": language, "topic": topic, "difficulty": difficulty},
        timeout=10,
    )
    response.raise_for_status()
    st.session_state.coding_question = response.json()


def run_coding_solution(code: str, language: str) -> None:
    response = requests.post(
        f"{BACKEND}/coding/run", json={"code": code, "language": language}, timeout=10
    )
    response.raise_for_status()
    st.session_state.coding_result = response.json()


def review_coding_solution(question: str, code: str, language: str) -> None:
    response = requests.post(
        f"{BACKEND}/coding/review",
        json={"question": question, "code": code, "language": language},
        timeout=10,
    )
    response.raise_for_status()
    st.session_state.coding_review = response.json()


def generate_system_design(topic: str, seniority: str, constraints: str) -> None:
    response = requests.post(
        f"{BACKEND}/system-design/generate",
        json={"topic": topic, "seniority": seniority, "constraints": constraints},
        timeout=10,
    )
    response.raise_for_status()
    st.session_state.system_design_prompt = response.json()


def review_system_design(topic: str, design_text: str) -> None:
    response = requests.post(
        f"{BACKEND}/system-design/review",
        json={"topic": topic, "design_text": design_text},
        timeout=10,
    )
    response.raise_for_status()
    st.session_state.system_design_review = response.json()


def calculate_salary(
    job_title: str,
    experience_years: int,
    location: str,
    company_type: str = "default",
    include_equity: bool = False,
) -> None:
    response = requests.post(
        f"{BACKEND}/salary/calculate",
        json={
            "job_title": job_title,
            "experience_years": experience_years,
            "location": location,
            "company_type": company_type,
            "include_equity": include_equity,
        },
        timeout=10,
    )
    response.raise_for_status()
    st.session_state.salary_result = response.json()


def generate_new_resume(profile: dict, template: str = "modern") -> None:
    response = requests.post(
        f"{BACKEND}/resume-builder/generate",
        json={**profile, "template": template},
        timeout=15,
    )
    response.raise_for_status()
    st.session_state.resume_builder_result = response.json()


def ask_career_coach(
    question: str, career_history: str = "", target_role: str = "", industry: str = ""
) -> None:
    response = requests.post(
        f"{BACKEND}/career/ask",
        json={
            "question": question,
            "career_history": career_history,
            "target_role": target_role,
            "industry": industry,
        },
        timeout=15,
    )
    response.raise_for_status()
    st.session_state.career_coach_response = response.json()


def get_career_path(industry: str, current_level: str) -> None:
    response = requests.get(
        f"{BACKEND}/career/career-path",
        params={"industry": industry, "current_level": current_level},
        timeout=10,
    )
    response.raise_for_status()
    st.session_state.career_path = response.json()


def start_phone_interview(
    role: str = "", focus: str = "general", audio_enabled: bool = True
) -> None:
    response = requests.post(
        f"{BACKEND}/phone-interview/start",
        json={"role": role, "focus": focus, "audio_enabled": audio_enabled},
        timeout=10,
    )
    response.raise_for_status()
    payload = response.json()
    st.session_state.phone_session_id = payload.get("session_id")
    st.session_state.phone_transcript = [
        {"speaker": "Interviewer", "message": payload.get("opening_prompt", "")}
    ]
    st.session_state.phone_scores = {
        "clarity": 0,
        "confidence": 0,
        "relevance": 0,
        "structure": 0,
    }


def send_phone_answer(message: str) -> None:
    response = requests.post(
        f"{BACKEND}/phone-interview/text",
        params={"session_id": st.session_state.phone_session_id, "message": message},
        timeout=10,
    )
    response.raise_for_status()
    payload = response.json()
    st.session_state.phone_transcript.extend(
        [
            {"speaker": "You", "message": message},
            {"speaker": "Interviewer", "message": payload.get("question", "")},
        ]
    )
    st.session_state.phone_scores = payload.get("scores", st.session_state.phone_scores)


def end_phone_interview() -> None:
    response = requests.post(
        f"{BACKEND}/phone-interview/end/{st.session_state.phone_session_id}", timeout=15
    )
    response.raise_for_status()
    st.session_state.analytics_result = response.json()
    st.session_state.phone_session_id = None
    st.session_state.phone_transcript = []
    st.session_state.phone_scores = None


def get_performance_analytics(transcript: list) -> None:
    response = requests.post(
        f"{BACKEND}/analytics/analyze",
        json={"session_id": "manual", "transcript": transcript},
        timeout=15,
    )
    response.raise_for_status()
    st.session_state.analytics_result = response.json()


def generate_stealth_hint(question: str) -> None:
    hints = [
        "Structure your answer using STAR method: Situation, Task, Action, Result",
        "Focus on quantifiable impact - use numbers and metrics",
        "Emphasize leadership and cross-functional collaboration",
        "Keep your answer under 2 minutes - be concise but thorough",
        "Connect your experience to the role requirements",
    ]
    import random

    hint = random.choice(hints)
    st.session_state.stealth_suggestions.append(
        {"question": question, "hint": hint, "timestamp": datetime.now().isoformat()}
    )


def generate_prep_plan(resume_text: str, target_role: str) -> None:
    st.session_state.prep_plan = {
        "target_role": target_role,
        "competencies": [
            "Leadership",
            "Problem Solving",
            "Communication",
            "Team Collaboration",
            "Strategic Thinking",
        ],
        "skills": [
            "Agile/Scrum",
            "Data Analysis",
            "Stakeholder Management",
            "Roadmap Planning",
            "Risk Mitigation",
        ],
        "sample_questions": [
            {
                "question": "Tell me about a time you led a challenging project",
                "framework": "STAR Method",
            },
            {
                "question": "How do you handle competing priorities?",
                "framework": "Priority Matrix + Examples",
            },
            {
                "question": "Describe your approach to stakeholder management",
                "framework": "Communication Framework",
            },
        ],
        "improvement_areas": [
            "Technical depth",
            "Case study practice",
            "STAR storytelling",
        ],
    }


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


def render_phase_indicator(current_phase: int) -> None:
    phases = [
        (1, "📝", "Onboarding"),
        (2, "🎯", "Practice"),
        (3, "🔴", "Live Mode"),
        (4, "📊", "Feedback"),
    ]

    html = '<div class="phase-indicator">'
    for i, (phase, icon, label) in enumerate(phases):
        if i > 0:
            html += '<div class="phase-connector"></div>'
        status = (
            "active"
            if phase == current_phase
            else ("completed" if phase < current_phase else "")
        )
        html += f'<div class="phase-step {status}">{icon} {label}</div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


initialize_state()
probe_backend()

st.markdown(
    """
<div class="hero-section">
    <div class="hero-badge">
        <span>🎯</span> AI-Powered Interview Preparation
    </div>
    <h1 class="hero-title">MyInterview AI</h1>
    <p class="hero-subtitle">
        Master your interviews with intelligent preparation, real-time stealth assistance, 
        and comprehensive performance analytics. Land your dream job with confidence.
    </p>
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-icon">📝</div>
            <div class="stat-value">10+</div>
            <div class="stat-label">Interview Modes</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">🎯</div>
            <div class="stat-value">95%</div>
            <div class="stat-label">Success Rate</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">⚡</div>
            <div class="stat-value">Real-time</div>
            <div class="stat-label">Stealth Mode</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">📊</div>
            <div class="stat-value">Deep</div>
            <div class="stat-label">Analytics</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">🚀</div>
            <div class="stat-value">AI</div>
            <div class="stat-label">Powered</div>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

if st.session_state.get("backend_status") != "ok":
    st.warning("Backend is offline. Some features may not work.")
else:
    st.success("✨ All systems operational - Ready to help you ace your interview!")

render_phase_indicator(st.session_state.current_phase)

with st.sidebar:
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); padding: 20px 15px; border-radius: 12px; text-align: center; margin-bottom: 15px;">
            <h2 style="color: white; margin: 0; font-size: 1.3rem;">🎯 Live Interview Copilot</h2>
            <p style="color: rgba(255,255,255,0.85); font-size: 0.8rem; margin: 8px 0 0 0;">AI-powered interview assistant</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("### 📋 Session Configuration")

    role_options = [
        "Product Manager",
        "Product Owner",
        "Tech Lead",
        "Software Engineer",
        "Data Scientist",
        "UX Designer",
    ]
    model_options = [
        "GPT-5",
        "GPT-4.1",
        "Claude 4.0 Sonnet",
        "Llama 3.1 8B",
        "Qwen 2.5 Coder",
    ]
    model_to_id = {
        "GPT-5": "gpt-5",
        "GPT-4.1": "gpt-4.1",
        "Claude 4.0 Sonnet": "claude-4-sonnet",
        "Llama 3.1 8B": "llama-3.1-8b",
        "Qwen 2.5 Coder": "qwen-2.5-coder",
    }
    tone_options = ["Professional", "Assertive", "Friendly"]
    format_options = ["Paragraph", "Bullet Point", "Short Answer", "Elaborated"]
    lang_options = ["English", "Spanish", "French", "German", "Chinese", "Japanese"]
    lang_to_code = {
        "English": "en",
        "Spanish": "es",
        "French": "fr",
        "German": "de",
        "Chinese": "zh",
        "Japanese": "ja",
    }
    materials_options = [
        "Agile Playbook",
        "Case Studies",
        "STAR Method",
        "Leadership Framework",
        "SMART Goals",
        "OKR Framework",
    ]

    current_config = st.session_state.get("copilot_config", {})

    st.markdown("**Role**")
    role_idx = (
        role_options.index(current_config.get("role", "Product Manager"))
        if current_config.get("role") in role_options
        else 0
    )
    selected_role = st.selectbox(
        "Target Role", role_options, index=role_idx, key="sidebar_role"
    )

    st.markdown("**AI Model**")
    model_idx = (
        model_options.index(current_config.get("model_display", "GPT-5"))
        if current_config.get("model_display") in model_options
        else 0
    )
    selected_model = st.selectbox(
        "AI Model", model_options, index=model_idx, key="sidebar_model"
    )

    st.markdown("**Tone & Format**")
    col_tone, col_format = st.columns(2)
    with col_tone:
        tone_idx = (
            tone_options.index(current_config.get("tone_display", "Professional"))
            if current_config.get("tone_display") in tone_options
            else 0
        )
        selected_tone = st.selectbox(
            "Tone", tone_options, index=tone_idx, key="sidebar_tone"
        )
    with col_format:
        format_idx = (
            format_options.index(current_config.get("format_display", "Paragraph"))
            if current_config.get("format_display") in format_options
            else 0
        )
        selected_format = st.selectbox(
            "Format", format_options, index=format_idx, key="sidebar_format"
        )

    st.markdown("**Language**")
    lang_idx = (
        lang_options.index(current_config.get("language_display", "English"))
        if current_config.get("language_display") in lang_options
        else 0
    )
    selected_language = st.selectbox(
        "Response Language", lang_options, index=lang_idx, key="sidebar_language"
    )

    st.markdown("---")
    st.markdown("### 🧠 Thinking Mode")

    thinking_mode = st.checkbox(
        "Enable Thinking Mode",
        value=current_config.get("thinking_mode", False),
        help="Shows internal reasoning before the answer",
        key="sidebar_thinking",
    )

    st.markdown("---")
    st.markdown("### 📄 Context")

    resume_input = st.text_area(
        "Resume (paste text)",
        value=current_config.get("resume", ""),
        height=80,
        placeholder="Paste your resume here...",
        key="sidebar_resume",
    )

    jd_input = st.text_area(
        "Job Description (optional)",
        value=current_config.get("jd", ""),
        height=80,
        placeholder="Paste job description...",
        key="sidebar_jd",
    )

    st.markdown("**Reference Materials**")
    selected_materials = st.multiselect(
        "Select materials",
        materials_options,
        default=current_config.get("materials", []),
        key="sidebar_materials",
    )

    st.markdown("")

    if st.button("🚀 Start Interview", type="primary", use_container_width=True):
        st.session_state.copilot_config = {
            "role": selected_role,
            "model": model_to_id.get(selected_model, "gpt-5"),
            "model_display": selected_model,
            "tone": selected_tone.lower(),
            "tone_display": selected_tone,
            "format": selected_format.lower().replace(" ", "_"),
            "format_display": selected_format,
            "language": lang_to_code.get(selected_language, "en"),
            "language_display": selected_language,
            "thinking_mode": thinking_mode,
            "resume": resume_input
            if resume_input
            else "Experienced professional with 5+ years in product management.",
            "jd": jd_input if jd_input else "",
            "materials": selected_materials,
        }

        try:
            response = requests.post(
                f"{BACKEND}/copilot/create-session",
                json={
                    "resume": {"text": resume_input}
                    if resume_input
                    else {
                        "text": "Experienced professional with 5+ years in product management."
                    },
                    "jd": jd_input if jd_input else "",
                    "role": selected_role,
                    "language": lang_to_code.get(selected_language, "en"),
                    "model": model_to_id.get(selected_model, "gpt-5"),
                    "tone": selected_tone.lower(),
                    "format": selected_format.lower().replace(" ", "_"),
                    "thinking_mode": thinking_mode,
                    "materials": selected_materials,
                },
                timeout=30,
            )
            if response.status_code == 200:
                session_data = response.json()
                st.session_state.copilot_session_id = session_data.get("session_id")
        except Exception:
            st.session_state.copilot_session_id = "temp"

        st.session_state.copilot_session_active = True
        st.session_state.copilot_answers = []
        st.session_state.active_tab = "🎯 Mock Interview"
        st.rerun()

    st.markdown("---")

    if st.button("🔄 Reset Session", use_container_width=True):
        st.session_state.copilot_config = {}
        st.session_state.copilot_session_active = False
        st.session_state.copilot_answers = []
        st.rerun()

    st.markdown("---")
    st.caption("💡 Tip: Start with behavioral questions like 'Tell me about yourself'")

if st.session_state.stealth_visible and st.session_state.stealth_mode:
    st.markdown(
        """
    <div class="stealth-panel visible">
        <div class="stealth-header">
            <div class="stealth-title">🕵️ Stealth Copilot</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    for i, suggestion in enumerate(st.session_state.stealth_suggestions[-5:]):
        st.markdown(
            f"""
        <div style="background: rgba(99, 102, 241, 0.08); border: 1px solid rgba(99, 102, 241, 0.15); 
                    border-radius: 12px; padding: 16px; margin-bottom: 12px;">
            <div style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 8px;">💡 Hint {i + 1}</div>
            <div style="color: var(--text-primary);">{suggestion["hint"]}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

st.markdown("---")

tab_options = [
    "🏠 Onboarding",
    "🎯 Mock Interview",
    "🔴 Stealth Mode",
    "📊 Analytics",
    "💼 JD & Resume",
    "💻 Technical",
    "💰 Career",
]

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "🏠 Onboarding"

try:
    default_index = tab_options.index(st.session_state.active_tab)
except ValueError:
    default_index = 0

selected_tab = st.selectbox(
    "Navigate to:",
    tab_options,
    index=default_index,
    key="tab_selector",
)

if selected_tab != st.session_state.active_tab:
    st.session_state.active_tab = selected_tab
    st.rerun()

main_tabs = st.tabs(tab_options)

(
    tab_onboarding,
    tab_interview,
    tab_stealth,
    tab_analytics,
    tab_jd_resume,
    tab_technical,
    tab_career,
) = main_tabs

with tab_onboarding:
    st.markdown('<div class="section-shell">', unsafe_allow_html=True)
    st.markdown("### 📝 Personalization & Onboarding")
    st.markdown(
        "*Upload your resume and target role to generate a personalized preparation plan.*"
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Step 1: Your Profile")
        onboarding_name = st.text_input("Full Name", placeholder="John Doe")
        onboarding_email = st.text_input("Email", placeholder="john@example.com")
        onboarding_role = st.text_input(
            "Target Role", placeholder="Senior Product Manager"
        )
        onboarding_industry = st.selectbox(
            "Industry",
            ["Tech", "Finance", "Healthcare", "Retail", "Consulting", "Other"],
        )

    with col2:
        st.markdown("#### Step 2: Upload Resume")
        onboarding_resume = st.file_uploader(
            "Resume File (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"]
        )
        onboarding_resume_text = st.text_area(
            "Or paste resume text", height=200, placeholder="Paste your resume here..."
        )

        if st.button("Generate Prep Plan", type="primary", use_container_width=True):
            if onboarding_resume_text.strip() and onboarding_role.strip():
                try:
                    generate_prep_plan(onboarding_resume_text, onboarding_role)
                    st.session_state.user_profile = {
                        "name": onboarding_name,
                        "email": onboarding_email,
                        "target_role": onboarding_role,
                        "industry": onboarding_industry,
                    }
                    st.session_state.current_phase = 2
                    st.success("Prep plan generated!")
                except Exception as exc:
                    st.error(f"Error: {exc}")
            else:
                st.warning("Please provide resume text and target role.")

    prep_plan = st.session_state.get("prep_plan")
    if prep_plan:
        st.markdown("---")
        st.markdown("#### 📋 Your Personalized Prep Plan")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**🎯 Key Competencies**")
            for c in prep_plan.get("competencies", []):
                st.write(f"✅ {c}")
        with col2:
            st.markdown("**💻 Technical Skills**")
            for s in prep_plan.get("skills", []):
                st.write(f"⚡ {s}")
        with col3:
            st.markdown("**📈 Improvement Areas**")
            for a in prep_plan.get("improvement_areas", []):
                st.write(f"📝 {a}")

        st.markdown("**❓ Sample Interview Questions**")
        for q in prep_plan.get("sample_questions", []):
            st.markdown(
                f"""
            <div style="background: rgba(99, 102, 241, 0.05); border-radius: 12px; padding: 16px; margin: 12px 0; border-left: 4px solid var(--accent-primary);">
                <div style="font-weight: 600; color: var(--accent-primary);">{q["question"]}</div>
                <div style="color: var(--text-muted); font-size: 0.85rem; margin-top: 8px;">Framework: {q["framework"]}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        if st.button(
            "🚀 Start Practice Session", type="primary", use_container_width=True
        ):
            st.session_state.current_phase = 2
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

with tab_interview:
    st.markdown('<div class="section-shell">', unsafe_allow_html=True)
    st.markdown("### 🎯 Live Interview Copilot")
    st.markdown("*Practice answering interview questions with AI-powered coaching.*")

    config = st.session_state.get("copilot_config", {})
    is_active = st.session_state.get("copilot_session_active", False)

    if is_active and config:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Role", config.get("role", "Not set"))
        with col2:
            st.metric("Model", config.get("model_display", "Not set"))
        with col3:
            st.metric("Tone", config.get("tone_display", "Not set"))
        with col4:
            st.metric("Format", config.get("format_display", "Not set"))

        st.markdown("---")

        st.markdown("#### 💬 Ask Your Interview Question")

        question = st.text_input(
            "Enter the interview question:",
            placeholder="e.g., Tell me about a time you led a team through a difficult challenge...",
            key="copilot_question",
        )

        col_q1, col_q2 = st.columns([1, 4])
        with col_q1:
            generate_btn = st.button(
                "🎯 Get Answer", type="primary", use_container_width=True
            )
        with col_q2:
            st.write("")

        if generate_btn and question:
            with st.spinner("Generating your answer..."):
                try:
                    response = requests.post(
                        f"{BACKEND}/copilot/generate-answer",
                        json={
                            "session_id": st.session_state.get(
                                "copilot_session_id", "temp"
                            ),
                            "question": question,
                        },
                        timeout=60,
                    )
                    if response.status_code == 200:
                        result = response.json()
                        st.session_state.copilot_current_answer = result.get(
                            "answer", ""
                        )
                        st.session_state.copilot_question = question
                        answers = st.session_state.get("copilot_answers", [])
                        answers.append(
                            {"question": question, "answer": result.get("answer", "")}
                        )
                        st.session_state.copilot_answers = answers
                    else:
                        result = generate_full_interview_answer(
                            question=question,
                            resume_context={
                                "skills": ["Leadership", "Communication"],
                                "achievements": ["Delivered projects"],
                            },
                            job_description=config.get("jd", ""),
                            role=config.get("role", "Product Manager"),
                            language=config.get("language", "en"),
                            model=config.get("model", "gpt-5"),
                            thinking_mode=config.get("thinking_mode", False),
                            answer_length=config.get("format", "paragraph"),
                            tone=config.get("tone", "professional"),
                            materials=config.get("materials", []),
                        )
                        st.session_state.copilot_current_answer = result.get(
                            "answer", ""
                        )
                        st.session_state.copilot_question = question
                        answers = st.session_state.get("copilot_answers", [])
                        answers.append(
                            {"question": question, "answer": result.get("answer", "")}
                        )
                        st.session_state.copilot_answers = answers
                except Exception as e:
                    st.error(f"Error generating answer: {str(e)}")
                    st.session_state.copilot_current_answer = ""

        if st.session_state.get("copilot_current_answer"):
            st.markdown("---")
            st.markdown("#### ✨ AI Answer")

            st.markdown(f"**Question:** {st.session_state.get('copilot_question', '')}")
            st.success(st.session_state.copilot_current_answer)

            col_r1, col_r2 = st.columns(2)
            with col_r1:
                st.write("**Settings Used:**")
                st.write(f"- Tone: {config.get('tone_display', 'Professional')}")
                st.write(f"- Format: {config.get('format_display', 'Paragraph')}")
                st.write(f"- Language: {config.get('language_display', 'English')}")
                st.write(
                    f"- Thinking Mode: {'On' if config.get('thinking_mode') else 'Off'}"
                )
            with col_r2:
                st.write("**Tips:**")
                st.write("• Use STAR method for behavioral questions")
                st.write("• Include specific metrics and examples")
                st.write("• Practice similar questions variations")

        st.markdown("---")
        st.markdown("#### 📜 Previous Answers")

        answers = st.session_state.get("copilot_answers", [])
        if answers:
            for i, ans in enumerate(reversed(answers[-5:])):
                with st.expander(f"Q: {ans['question'][:50]}...", expanded=False):
                    st.markdown(f"**Question:** {ans['question']}")
                    st.markdown(f"**Answer:** {ans['answer']}")
        else:
            st.info("No answers generated yet. Ask your first question above!")

    else:
        st.info(
            "👈 Configure your interview settings in the sidebar and click '🚀 Start Interview' to begin."
        )

        st.markdown("---")
        st.markdown("#### 📝 Sample Questions to Practice")

        sample_questions = [
            "Tell me about yourself and your background.",
            "Describe a time you led a team through a challenging project.",
            "How do you prioritize competing deadlines?",
            "Tell me about a time you had a conflict with a colleague.",
            "Describe your greatest professional achievement.",
            "How do you handle feedback and criticism?",
            "Where do you see yourself in 5 years?",
            "Why are you interested in this role/company?",
        ]

        col_q1, col_q2 = st.columns(2)
        for i, q in enumerate(sample_questions):
            with col_q1 if i % 2 == 0 else col_q2:
                st.markdown(f"• {q}")

    st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("🎤 Live Interview Copilot", expanded=True):
        st.markdown("### AI-Powered Live Interview Assistant")

        quick_setup = st.session_state.get("quick_setup", {})

        if quick_setup:
            st.markdown("**Current Configuration:**")
            config_col1, config_col2 = st.columns(2)
            with config_col1:
                st.write(f"**Role:** {quick_setup.get('role', 'Not set')}")
                st.write(
                    f"**Model:** {quick_setup.get('_model_display', quick_setup.get('model', 'Not set'))}"
                )
                st.write(
                    f"**Tone:** {quick_setup.get('_tone_display', quick_setup.get('tone', 'Not set'))}"
                )
            with config_col2:
                st.write(
                    f"**Format:** {quick_setup.get('_length_display', quick_setup.get('length', 'Not set'))}"
                )
                st.write(
                    f"**Thinking:** {'On' if quick_setup.get('thinking_mode') else 'Off'}"
                )
                st.write(
                    f"**Language:** {quick_setup.get('_lang_display', quick_setup.get('language', 'Not set'))}"
                )
        else:
            st.info(
                "Configure interview settings in the sidebar and click 'Start Interview'"
            )

        st.markdown("---")
        st.markdown("### Ask a Question")

        question_input = st.text_input(
            "Enter interview question:",
            placeholder="e.g., Tell me about a time you showed leadership...",
        )

        if st.button("Get AI Answer", type="primary", use_container_width=True):
            if question_input.strip():
                with st.spinner("Generating answer..."):
                    try:
                        setup = st.session_state.get("quick_setup", {})
                        answer_result = generate_full_interview_answer(
                            question=question_input,
                            resume_context={
                                "skills": [
                                    "Agile",
                                    "Leadership",
                                    "Stakeholder Management",
                                ],
                                "achievements": [
                                    "Delivered 10+ projects",
                                    "Increased team productivity",
                                ],
                            },
                            job_description=setup.get("jd", "") if setup else "",
                            role=setup.get("role", "Product Manager")
                            if setup
                            else "Product Manager",
                            language=setup.get("language", "en") if setup else "en",
                            model=setup.get("model", "gpt-5") if setup else "gpt-5",
                            category="behavioral",
                            thinking_mode=setup.get("thinking_mode", False)
                            if setup
                            else False,
                            answer_length=setup.get("length", "paragraph")
                            if setup
                            else "paragraph",
                            tone=setup.get("tone", "professional")
                            if setup
                            else "professional",
                            materials=setup.get("materials", []) if setup else [],
                        )
                        st.session_state.last_answer = answer_result
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Please enter a question first")

        if st.session_state.get("last_answer"):
            result = st.session_state.last_answer
            st.markdown("---")
            st.markdown("### AI Generated Answer")

            st.markdown("**Question:**")
            st.info(question_input if question_input else "Previous question")

            st.markdown("**Answer:**")
            st.success(result.get("answer", ""))

            st.markdown("**Settings Used:**")
            settings = result.get("settings", {})
            ctx = result.get("context_used", {})
            st.write(f"- Tone: {settings.get('tone', 'N/A').title()}")
            st.write(
                f"- Format: {settings.get('length', 'N/A').replace('_', ' ').title()}"
            )
            st.write(f"- Category: {result.get('category', 'N/A').title()}")
            st.write(
                f"- Thinking Mode: {'On' if settings.get('thinking_mode') else 'Off'}"
            )

    st.markdown("---")
    st.markdown("#### 💡 Quick Tips")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("**STAR Method**\nSituation → Task → Action → Result")
    with col2:
        st.markdown("**Quantify Impact**\nUse numbers and metrics")
    with col3:
        st.markdown("**Be Concise**\nUnder 2 minutes per answer")
    with col4:
        st.markdown("**Show Growth**\nEnd with lessons learned")

    st.markdown("</div>", unsafe_allow_html=True)

with tab_stealth:
    st.markdown('<div class="section-shell">', unsafe_allow_html=True)
    st.markdown("### 🔴 Stealth Mode - Live Interview Copilot")
    st.markdown(
        "*Get hidden AI assistance during real interviews. Completely invisible to interviewers.*"
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(
            """
        <div class="info-box">
            <h4>🕵️ How Stealth Mode Works</h4>
            <ol style="color: var(--text-secondary); line-height: 2;">
                <li>Enable Stealth Mode from the sidebar</li>
                <li>Start your interview preparation session</li>
                <li>AI analyzes questions in real-time</li>
                <li>Structured answer hints appear discreetly</li>
                <li>Tips visible only to you - undetectable!</li>
            </ol>
            <p style="color: var(--accent-success); font-weight: 600; margin-top: 16px;">✅ Works with any video conferencing platform</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown("#### 🎯 Stealth Features")
        features = [
            ("Real-time Question Analysis", "Understand what's being asked"),
            ("STAR Framework Hints", "Structured answer templates"),
            ("Quantification Tips", "Add metrics to answers"),
            ("Body Language Cues", "Subtle confidence boosters"),
            ("Follow-up Suggestions", "Handle curveballs"),
        ]
        for feat, desc in features:
            st.markdown(f"**{feat}**: {desc}")

    with col2:
        st.markdown("#### 🚀 Start Stealth Session")

        user_profile = st.session_state.get("user_profile") or {}
        stealth_role = st.text_input(
            "Target Role",
            value=user_profile.get("target_role", "Product Manager")
            or "Product Manager",
        )
        stealth_focus = st.text_input(
            "Focus Areas", value="leadership, problem-solving, communication"
        )

        if st.button(
            "Launch Stealth Copilot", type="primary", use_container_width=True
        ):
            try:
                start_live_copilot(stealth_role, stealth_focus)
                st.session_state.stealth_mode = True
                st.session_state.current_phase = 3
                st.success("Stealth Copilot launched!")
                st.rerun()
            except requests.RequestException as exc:
                st.error(f"Error: {exc}")

        st.markdown("---")
        st.markdown("#### 📋 Live Session Transcript")
        transcript = st.session_state.get("copilot_transcript", [])
        if transcript:
            for item in transcript:
                speaker = item["speaker"]
                bubble_class = "chat-you" if speaker == "You" else "chat-ai"
                st.markdown(
                    f'<div class="chat-bubble {bubble_class}"><div class="chat-speaker">{speaker}</div><div>{item["message"]}</div></div>',
                    unsafe_allow_html=True,
                )

        stealth_answer = st.text_area(
            "Your Answer (for hint generation)",
            height=120,
            placeholder="Type your live interview answer...",
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Submit & Get Hint", use_container_width=True):
                if stealth_answer.strip():
                    try:
                        send_copilot_answer(stealth_answer)
                        generate_stealth_hint(stealth_answer)
                        st.rerun()
                    except requests.RequestException as exc:
                        st.error(f"Error: {exc}")
        with col2:
            if st.button("Get Feedback", use_container_width=True):
                if stealth_answer.strip():
                    try:
                        review_copilot_answer(stealth_answer)
                    except requests.RequestException as exc:
                        st.error(f"Error: {exc}")

        feedback = st.session_state.get("copilot_feedback")
        if feedback:
            st.markdown("#### 📊 Feedback")
            st.json(feedback)

    st.markdown("</div>", unsafe_allow_html=True)

with tab_analytics:
    st.markdown('<div class="section-shell">', unsafe_allow_html=True)
    st.markdown("### 📊 Post-Interview Analytics")
    st.markdown(
        "*Detailed performance analysis with personalized improvement roadmaps.*"
    )

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("#### Analyze Interview Transcript")
        analytics_text = st.text_area(
            "Paste Interview Transcript",
            height=200,
            placeholder="You: I led a team of 5 engineers...\nInterviewer: How did you handle the conflict?\nYou: I organized a meeting...",
        )
    if st.button("Analyze Performance", type="primary", use_container_width=True):
        try:
            transcript = []
            for line in analytics_text.split("\n"):
                if ": " in line:
                    speaker, text = line.split(": ", 1)
                    speaker = speaker.strip()
                    if speaker.lower() == "you" or speaker.lower() == "candidate":
                        speaker = "candidate"
                    transcript.append({"speaker": speaker, "text": text.strip()})
            get_performance_analytics(transcript)
            st.session_state.current_phase = 4
        except requests.RequestException as exc:
            st.error(f"Error: {exc}")

    with col2:
        st.markdown("#### Performance Score")
        analytics = st.session_state.get("analytics_result")
        if analytics:
            score = analytics.get("overall_score", 75)
            st.markdown(
                f"""
            <div class="progress-ring-container">
                <div class="progress-ring" style="background: conic-gradient(var(--accent-primary) {score}%, var(--bg-tertiary) {score}%);">
                    <div class="progress-value">{score}</div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.info("No analysis yet")

    analytics = st.session_state.get("analytics_result")
    if analytics:
        st.markdown("---")
        st.markdown("#### 📋 Detailed Analysis")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Overall", f"{analytics.get('overall_score', 0):.1f}/100")
        with col2:
            st.metric(
                "STAR Usage",
                f"{analytics.get('star_analysis', {}).get('star_usage_percentage', 0):.1f}%",
            )
        with col3:
            st.metric(
                "Clarity",
                f"{analytics.get('speech_analysis', {}).get('clarity_score', 0):.1f}",
            )
        with col4:
            st.metric(
                "Confidence",
                f"{analytics.get('speech_analysis', {}).get('confidence_score', 0):.1f}",
            )

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### ✅ Strengths")
            for s in analytics.get("strengths", []):
                st.success(f"✓ {s}")
        with col2:
            st.markdown("#### 📝 Areas for Improvement")
            for i in analytics.get("improvements", []):
                st.warning(f"• {i}")

        st.markdown("---")
        st.markdown("#### 🗺️ Personalized Improvement Roadmap")

        roadmap = [
            (
                "Week 1-2",
                "STAR Method Mastery",
                "Practice 5 behavioral questions daily using STAR framework",
            ),
            (
                "Week 3-4",
                "Quantification Skills",
                "Learn to add metrics and impact to every answer",
            ),
            ("Week 5-6", "Body Language", "Practice confident posture and eye contact"),
            (
                "Week 7-8",
                "Mock Interviews",
                "Complete 3 full mock interviews with feedback",
            ),
        ]

        for week, title, desc in roadmap:
            st.markdown(
                f"""
            <div class="roadmap-card">
                <div class="roadmap-week">{week}</div>
                <div class="roadmap-content">
                    <h4>{title}</h4>
                    <p>{desc}</p>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        if st.button("🔄 Start New Session", type="primary", use_container_width=True):
            st.session_state.current_phase = 1
            st.session_state.analytics_result = None
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

with tab_jd_resume:
    st.markdown('<div class="section-shell">', unsafe_allow_html=True)
    st.markdown("### 💼 JD Intelligence & Resume Review")

    sub_tabs = st.tabs(
        ["📋 JD Analysis", "📄 Resume Review", "✨ Resume Builder", "🔍 RAG Search"]
    )

    with sub_tabs[0]:
        st.markdown("#### Job Description Analysis")
        jd_text = st.text_area(
            "Paste Job Description", height=200, placeholder="Paste JD here..."
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Prepare Questions", type="primary", use_container_width=True):
                if jd_text.strip():
                    try:
                        generate_ai_jd_questions(jd_text)
                        st.rerun()
                    except requests.RequestException as exc:
                        st.error(f"Error: {exc}")
        with col2:
            if st.button("Start Mock Interview", use_container_width=True):
                if jd_text.strip():
                    try:
                        generate_jd_interview(jd_text)
                        st.rerun()
                    except requests.RequestException as exc:
                        st.error(f"Error: {exc}")

        st.caption(
            "**Prepare Questions** = Study material with answers & tips | **Start Mock Interview** = Practice session with opening prompt"
        )

        jd_analysis = st.session_state.get("jd_analysis")
        jd_interview = st.session_state.get("jd_interview")

        if jd_analysis:
            st.markdown("#### Analysis Results")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Skills Found", len(jd_analysis.get("skills", [])))
            with col2:
                st.metric("Competencies", len(jd_analysis.get("competencies", [])))
            with col3:
                st.metric("Categories", len(jd_analysis.get("question_categories", {})))

            st.markdown("**Summary**")
            st.write(jd_analysis.get("summary", ""))

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Key Skills**")
                for skill in jd_analysis.get("skills", []):
                    st.write(f"- {skill}")
            with col2:
                st.markdown("**Core Competencies**")
                for comp in jd_analysis.get("competencies", []):
                    st.write(f"- {comp}")

        ai_questions = st.session_state.get("ai_jd_questions")
        if ai_questions:
            st.markdown("---")
            st.markdown("#### AI-Generated Interview Questions with Answers")

            questions_data = ai_questions.get("questions", {})
            answers_data = ai_questions.get("answers", {})
            competencies = ai_questions.get("competencies", [])

            if competencies:
                st.markdown(f"**Target Competencies:** {', '.join(competencies)}")

            ai_category_names = [
                ("behavioral_questions", "Behavioral Questions", "green"),
                ("delivery_questions", "Delivery Questions", "blue"),
                ("leadership_questions", "Leadership Questions", "purple"),
                ("execution_questions", "Execution Questions", "orange"),
                ("risk_mitigation_questions", "Risk Mitigation Questions", "red"),
                ("follow_up_questions", "Follow-up Questions", "gray"),
            ]

            for key, label, color in ai_category_names:
                questions = questions_data.get(key, [])
                cat_answers = answers_data.get(key, {})
                if questions:
                    st.markdown(f"### {label} ({len(questions)})")
                    for i, q in enumerate(questions):
                        st.markdown(f"**Q{i + 1}:** {q}")

                        answer = cat_answers.get(str(i), {})
                        if answer:
                            col_a, col_b = st.columns(2)
                            with col_a:
                                st.markdown("**Key Points:**")
                                for point in answer.get("key_points", []):
                                    st.markdown(f"- {point}")
                            with col_b:
                                st.markdown("**Tips:**")
                                for tip in answer.get("tips", []):
                                    st.markdown(f"- {tip}")
                            st.markdown("**Sample Answer:**")
                            st.info(answer.get("sample_answer", ""))

                            follow_ups = answer.get("follow_up_questions", [])
                            follow_up_answers = answer.get("follow_up_answers", {})
                            if follow_ups:
                                st.markdown("")
                                st.markdown(
                                    "**Interviewer Follow-up Questions with Suggested Answers:**"
                                )
                                for idx, fq in enumerate(follow_ups, 1):
                                    fq_answer = follow_up_answers.get(
                                        fq,
                                        "Prepare your own concise 30-second response focusing on specifics and outcomes.",
                                    )
                                    st.markdown(f"**Follow-up {idx}:** {fq}")
                                    st.success(fq_answer)
                                    st.markdown("")
                        st.markdown("")
                    st.markdown("---")

        if jd_interview:
            st.markdown("---")
            st.markdown("#### Generated Interview Package")

            st.markdown("**Opening Prompt**")
            st.info(jd_interview.get("opening_prompt", ""))

            profile = jd_interview.get("profile", {})
            categories = profile.get("question_categories", {})

            if categories:
                st.markdown("**Interview Questions by Category**")

                category_names = {
                    "behavioral_questions": "🟢 Behavioral Questions",
                    "delivery_questions": "🔵 Delivery Questions",
                    "leadership_questions": "🟣 Leadership Questions",
                    "execution_questions": "🟡 Execution Questions",
                    "risk_mitigation_questions": "🔴 Risk Mitigation",
                    "follow_up_questions": "⚪ Follow-up Questions",
                }

                for key, label in category_names.items():
                    questions = categories.get(key, [])
                    if questions:
                        with st.expander(label):
                            for q in questions:
                                st.write(f"- {q}")

            scenarios = profile.get("scenarios", [])
            if scenarios:
                st.markdown("**Interview Scenarios**")
                for i, scenario in enumerate(scenarios, 1):
                    st.write(f"{i}. {scenario}")

        if not jd_analysis and not jd_interview:
            st.info("Analyze a job description to see results here.")

    with sub_tabs[1]:
        st.markdown("#### Resume Review")
        resume_text = st.text_area("Paste Resume", height=200)
        resume_file = st.file_uploader("Or upload Resume", type=["pdf", "docx", "txt"])

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Analyze Resume", type="primary", use_container_width=True):
                if resume_text.strip():
                    try:
                        analyze_resume(resume_text)
                    except requests.RequestException as exc:
                        st.error(f"Error: {exc}")
        with col2:
            if st.button("Generate Questions", use_container_width=True):
                if resume_file:
                    try:
                        generate_resume_questions(resume_file)
                    except requests.RequestException as exc:
                        st.error(f"Error: {exc}")
        with col3:
            if st.button("Create Prep Plan", use_container_width=True):
                if resume_text.strip():
                    generate_prep_plan(resume_text, "Target Role")
                    st.rerun()

        if st.session_state.get("resume_analysis"):
            st.markdown("#### Analysis")
            st.write(st.session_state.resume_analysis.get("analysis", ""))

        if st.session_state.get("resume_questions"):
            st.markdown("#### Generated Questions")
            render_question_groups(
                st.session_state.resume_questions.get("questions", {})
            )

    with sub_tabs[2]:
        st.markdown("#### AI Resume Builder")
        col1, col2 = st.columns(2)
        with col1:
            rb_name = st.text_input("Full Name")
            rb_email = st.text_input("Email")
            rb_phone = st.text_input("Phone")
        with col2:
            rb_role = st.text_input("Target Role")
            rb_template = st.selectbox(
                "Template", ["modern", "classic", "minimal", "executive"]
            )

        rb_summary = st.text_area("Professional Summary", height=100)
        rb_skills = st.text_area("Skills (comma separated)", height=80)

        if st.button("Generate Resume", type="primary", use_container_width=True):
            try:
                skills_list = [s.strip() for s in rb_skills.split(",") if s.strip()]
                generate_new_resume(
                    {
                        "name": rb_name,
                        "email": rb_email,
                        "phone": rb_phone,
                        "summary": rb_summary,
                        "target_role": rb_role,
                        "skills": skills_list,
                    },
                    rb_template,
                )
            except requests.RequestException as exc:
                st.error(f"Error: {exc}")

        if st.session_state.get("resume_builder_result"):
            st.markdown("#### Generated Resume")
            st.text_area(
                "Content",
                value=st.session_state.resume_builder_result.get("preview_text", ""),
                height=400,
            )

    with sub_tabs[3]:
        st.markdown("#### RAG Context Search")
        rag_query = st.text_input(
            "Search Query", placeholder="stakeholder management..."
        )
        if st.button("Search", type="primary", use_container_width=True):
            if rag_query.strip():
                try:
                    search_rag(rag_query)
                except requests.RequestException as exc:
                    st.error(f"Error: {exc}")

        if st.session_state.get("rag_context"):
            st.code(st.session_state.rag_context)

    st.markdown("</div>", unsafe_allow_html=True)

with tab_technical:
    st.markdown('<div class="section-shell">', unsafe_allow_html=True)
    st.markdown("### 💻 Technical Interview Practice")

    sub_tabs = st.tabs(["💻 Coding Lab", "🏗️ System Design", "🎤 Voice Tools"])

    with sub_tabs[0]:
        st.markdown("#### Coding Interview Lab")
        col1, col2, col3 = st.columns(3)
        with col1:
            lang = st.selectbox("Language", ["python", "javascript", "java"], index=0)
        with col2:
            topic = st.selectbox("Topic", ["arrays", "strings", "graphs"], index=0)
        with col3:
            diff = st.selectbox("Difficulty", ["easy", "medium", "hard"], index=1)

        if st.button("Generate Question", type="primary", use_container_width=True):
            try:
                generate_coding_question(lang, topic, diff)
            except requests.RequestException as exc:
                st.error(f"Error: {exc}")

        q = st.session_state.get("coding_question")
        q_text = ""
        if q:
            q_text = q.get("question", "")
            st.markdown("#### Question")
            st.write(q_text)

        code = st.text_area("Your Solution", height=200)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Run Code", use_container_width=True):
                if code.strip():
                    try:
                        run_coding_solution(code, lang)
                    except requests.RequestException as exc:
                        st.error(f"Error: {exc}")
        with col2:
            if st.button("Review", use_container_width=True):
                if q_text and code.strip():
                    try:
                        review_coding_solution(q_text, code, lang)
                    except requests.RequestException as exc:
                        st.error(f"Error: {exc}")

        if st.session_state.get("coding_result"):
            st.markdown("#### Result")
            st.json(st.session_state.coding_result)
        if st.session_state.get("coding_review"):
            st.markdown("#### Review")
            st.json(st.session_state.coding_review)

    with sub_tabs[1]:
        st.markdown("#### System Design Interview")
        sd_topic = st.text_input("Topic", placeholder="Design a URL shortener")
        col1, col2 = st.columns(2)
        with col1:
            sd_level = st.selectbox("Seniority", ["mid", "senior", "staff"], index=0)
        with col2:
            sd_constraints = st.text_input(
                "Constraints", placeholder="Global traffic..."
            )

        if st.button("Generate Prompt", type="primary", use_container_width=True):
            if sd_topic.strip():
                try:
                    generate_system_design(sd_topic, sd_level, sd_constraints)
                except requests.RequestException as exc:
                    st.error(f"Error: {exc}")

        sd = st.session_state.get("system_design_prompt")
        if sd:
            st.markdown("#### Prompt")
            st.write(sd.get("prompt", ""))
            if sd.get("mermaid_diagram"):
                st.code(sd.get("mermaid_diagram"), language="mermaid")

        sd_ans = st.text_area("Your Design", height=150)
        if st.button("Review Design", use_container_width=True):
            if sd_topic and sd_ans.strip():
                try:
                    review_system_design(sd_topic, sd_ans)
                except requests.RequestException as exc:
                    st.error(f"Error: {exc}")

        if st.session_state.get("system_design_review"):
            st.markdown("#### Review")
            st.json(st.session_state.system_design_review)

    with sub_tabs[2]:
        st.markdown("#### Voice Tools")
        col1, col2 = st.columns(2)
        with col1:
            tts = st.text_area("Text for Speech", height=100)
            if st.button("Generate Speech", type="primary", use_container_width=True):
                if tts.strip():
                    try:
                        synthesize_voice(tts)
                    except requests.RequestException as exc:
                        st.error(f"Error: {exc}")
            if st.session_state.get("voice_tts_result"):
                audio = st.session_state.voice_tts_result.get("audio_file", "")
                if audio:
                    st.audio(f"{BACKEND_ROOT}/{audio.replace(chr(92), '/')}")
        with col2:
            stt_file = st.file_uploader("Upload Audio", type=["wav", "mp3", "m4a"])
            if st.button("Transcribe", use_container_width=True):
                if stt_file:
                    try:
                        transcribe_voice(stt_file)
                    except requests.RequestException as exc:
                        st.error(f"Error: {exc}")
            if st.session_state.get("voice_stt_result"):
                st.write(st.session_state.voice_stt_result.get("text", ""))

    st.markdown("</div>", unsafe_allow_html=True)

with tab_career:
    st.markdown('<div class="section-shell">', unsafe_allow_html=True)
    st.markdown("### 💰 Career Development Tools")

    sub_tabs = st.tabs(["💰 Salary", "🎓 Career Coach", "📞 Phone Interview"])

    with sub_tabs[0]:
        st.markdown("#### Salary Calculator")
        col1, col2, col3 = st.columns(3)
        with col1:
            s_job = st.text_input("Job Title", placeholder="Software Engineer")
        with col2:
            s_exp = st.number_input("Years Experience", 0, 50, 5)
        with col3:
            s_loc = st.text_input("Location", placeholder="USA")
        col1, col2 = st.columns(2)
        with col1:
            s_company = st.selectbox(
                "Company Type",
                ["default", "startup", "tech_large", "finance", "consulting"],
            )
        with col2:
            s_equity = st.checkbox("Include Equity")

        if st.button("Calculate", type="primary", use_container_width=True):
            try:
                calculate_salary(s_job, s_exp, s_loc, s_company, s_equity)
            except requests.RequestException as exc:
                st.error(f"Error: {exc}")

        s = st.session_state.get("salary_result")
        if s:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    "Base", f"{s.get('currency', 'USD')} {s.get('base_salary', 0):,}"
                )
            with col2:
                st.metric("Bonus", f"{s.get('bonus', 0):,}")
            with col3:
                st.metric("Total", f"{s.get('total_cash', 0):,}")
            st.markdown("**Tips:**")
            for t in s.get("negotiation_tips", []):
                st.write(f"- {t}")

    with sub_tabs[1]:
        st.markdown("#### AI Career Coach")
        cc_q = st.text_area(
            "Your Question", height=100, placeholder="How do I transition to PM?"
        )
        cc_history = st.text_area("Career History (optional)", height=80)
        col1, col2 = st.columns(2)
        with col1:
            cc_role = st.text_input("Target Role (optional)")
        with col2:
            cc_industry = st.text_input("Industry (optional)")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Ask Coach", type="primary", use_container_width=True):
                try:
                    ask_career_coach(cc_q, cc_history, cc_role, cc_industry)
                except requests.RequestException as exc:
                    st.error(f"Error: {exc}")
        with col2:
            if st.button("Get Career Path", use_container_width=True):
                try:
                    get_career_path(cc_industry or "tech", "mid")
                except requests.RequestException as exc:
                    st.error(f"Error: {exc}")

        if st.session_state.get("career_coach_response"):
            st.markdown("#### Advice")
            st.write(st.session_state.career_coach_response.get("response", ""))
        if st.session_state.get("career_path"):
            st.markdown("#### Career Progression")
            for level, roles in st.session_state.career_path.get(
                "career_progression", {}
            ).items():
                st.markdown(f"**{level.title()}**: {', '.join(roles)}")

    with sub_tabs[2]:
        st.markdown("#### Phone Interview Assistant")
        col1, col2 = st.columns(2)
        with col1:
            p_role = st.text_input("Role", value="Product Manager")
        with col2:
            p_focus = st.text_input("Focus", value="general")

        if not st.session_state.get("phone_session_id"):
            if st.button("Start Interview", type="primary", use_container_width=True):
                try:
                    start_phone_interview(p_role, p_focus, True)
                    st.rerun()
                except requests.RequestException as exc:
                    st.error(f"Error: {exc}")
        else:
            st.success("Interview in progress...")
            if st.button("End Interview", use_container_width=True):
                try:
                    end_phone_interview()
                    st.rerun()
                except requests.RequestException as exc:
                    st.error(f"Error: {exc}")

        for item in st.session_state.get("phone_transcript", []):
            bc = "chat-you" if item["speaker"] == "You" else "chat-ai"
            st.markdown(
                f'<div class="chat-bubble {bc}"><div class="chat-speaker">{item["speaker"]}</div><div>{item["message"]}</div></div>',
                unsafe_allow_html=True,
            )

        p_ans = st.text_area("Your Answer", height=100)
        if st.button("Submit", use_container_width=True) and st.session_state.get(
            "phone_session_id"
        ):
            try:
                send_phone_answer(p_ans)
                st.rerun()
            except requests.RequestException as exc:
                st.error(f"Error: {exc}")

        scores = st.session_state.get("phone_scores")
        if scores:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Clarity", f"{scores.get('clarity', 0):.0f}")
            with col2:
                st.metric("Confidence", f"{scores.get('confidence', 0):.0f}")
            with col3:
                st.metric("Relevance", f"{scores.get('relevance', 0):.0f}")
            with col4:
                st.metric("Structure", f"{scores.get('structure', 0):.0f}")

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown(
    """
<div style="text-align: center; color: var(--text-muted); padding: 24px 0; font-size: 0.9rem;">
    <p><strong>MyInterview AI</strong> - Your AI-Powered Interview Companion</p>
    <p style="color: var(--text-light);">Built with FastAPI, Streamlit, and LangChain</p>
</div>
""",
    unsafe_allow_html=True,
)
