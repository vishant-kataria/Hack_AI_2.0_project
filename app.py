import streamlit as st
import pandas as pd
import time
import datetime
import random
import database as db  # SQLite database module

# -----------------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------------
st.set_page_config(
    page_title="CareerForge — AI Career Coach",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------------------------------------------
# CUSTOM CSS — Premium Dark Theme
# -----------------------------------------------------------------
def load_css():
    st.markdown("""
    <style>
    /* ——— Google Font ——— */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');

    /* ——— Root variables ——— */
    :root {
        --bg: #0a0e1a;
        --card: #111827;
        --card-hover: #1e293b;
        --accent: #6366f1;
        --accent-light: #818cf8;
        --accent-glow: rgba(99,102,241,0.4);
        --text: #f1f5f9;
        --text-dim: #94a3b8;
        --success: #22c55e;
        --warning: #f59e0b;
        --danger: #ef4444;
        --radius: 16px;
        --radius-sm: 10px;
        --purple: #7c3aed;
        --cyan: #06b6d4;
        --rose: #f43f5e;
    }

    /* ——— Global ——— */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 1200px !important;
    }

    /* ——— Hide Streamlit branding ——— */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ——— Tab styling ——— */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: var(--card);
        border-radius: var(--radius);
        padding: 6px;
        border: 1px solid rgba(255,255,255,0.06);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: var(--radius-sm);
        padding: 10px 18px;
        font-weight: 500;
        font-size: 0.85rem;
        color: var(--text-dim);
        background: transparent;
        border: none;
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--text);
        background: rgba(99,102,241,0.1);
    }
    .stTabs [aria-selected="true"] {
        background: var(--accent) !important;
        color: white !important;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(99,102,241,0.35);
    }
    .stTabs [data-baseweb="tab-highlight"] {
        display: none;
    }
    .stTabs [data-baseweb="tab-border"] {
        display: none;
    }

    /* ——— Card component ——— */
    .card {
        background: var(--card);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: var(--radius);
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.2);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }

    /* ——— Metric card ——— */
    .metric-card {
        background: var(--card);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: var(--radius);
        padding: 20px 24px;
        text-align: center;
        box-shadow: 0 4px 24px rgba(0,0,0,0.2);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        border-color: var(--accent);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--accent), var(--accent-light));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 8px 0 4px;
    }
    .metric-label {
        font-size: 0.8rem;
        color: var(--text-dim);
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 600;
    }
    .metric-delta {
        font-size: 0.78rem;
        color: var(--success);
        margin-top: 4px;
    }

    /* ——— AI Insight box ——— */
    .ai-insight {
        background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(139,92,246,0.1));
        border: 1px solid rgba(99,102,241,0.25);
        border-left: 4px solid var(--accent);
        border-radius: var(--radius);
        padding: 24px 28px;
        margin: 20px 0;
        box-shadow: 0 4px 20px rgba(99,102,241,0.1);
    }
    .ai-insight h4 {
        margin: 0 0 8px 0;
        color: var(--accent-light);
        font-size: 0.9rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .ai-insight p {
        margin: 0;
        font-size: 1.05rem;
        color: var(--text);
        line-height: 1.6;
    }

    /* ——— Smart alert ——— */
    .smart-alert {
        background: linear-gradient(135deg, rgba(245,158,11,0.12), rgba(239,68,68,0.08));
        border: 1px solid rgba(245,158,11,0.25);
        border-left: 4px solid var(--warning);
        border-radius: var(--radius);
        padding: 16px 22px;
        margin-bottom: 20px;
        font-size: 0.95rem;
        color: var(--text);
    }

    /* ——— Hero section ——— */
    .hero {
        text-align: center;
        padding: 36px 20px 28px;
    }
    .hero h1 {
        font-size: 3rem;
        font-weight: 900;
        margin: 0;
        background: linear-gradient(135deg, #fff, var(--accent-light));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
    }
    .hero p {
        font-size: 1.15rem;
        color: var(--text-dim);
        margin: 12px 0 0;
        font-weight: 400;
    }

    /* ——— Skill tag ——— */
    .skill-tag {
        display: inline-block;
        background: linear-gradient(135deg, rgba(99,102,241,0.2), rgba(99,102,241,0.08));
        border: 1px solid rgba(99,102,241,0.3);
        color: var(--accent-light);
        padding: 6px 14px;
        border-radius: 20px;
        margin: 4px;
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.3px;
        transition: all 0.2s ease;
    }
    .skill-tag:hover {
        background: rgba(99,102,241,0.3);
        transform: scale(1.05);
    }

    /* ——— Day card for roadmap ——— */
    .day-card {
        background: var(--card);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: var(--radius);
        padding: 20px 24px;
        margin-bottom: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.15);
        transition: border-color 0.2s ease;
    }
    .day-card:hover {
        border-color: var(--accent);
    }
    .day-card .day-title {
        font-size: 1rem;
        font-weight: 700;
        color: var(--text);
        margin-bottom: 4px;
    }
    .day-card .day-focus {
        font-size: 0.85rem;
        color: var(--text-dim);
        margin-bottom: 10px;
    }

    /* Difficulty badges */
    .badge-easy {
        background: rgba(34,197,94,0.15);
        color: #22c55e;
        padding: 3px 10px;
        border-radius: 8px;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
    }
    .badge-medium {
        background: rgba(245,158,11,0.15);
        color: #f59e0b;
        padding: 3px 10px;
        border-radius: 8px;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
    }
    .badge-hard {
        background: rgba(239,68,68,0.15);
        color: #ef4444;
        padding: 3px 10px;
        border-radius: 8px;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
    }

    /* ——— Chat bubbles ——— */
    .chat-user {
        background: var(--accent);
        color: white;
        padding: 14px 18px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0;
        max-width: 80%;
        margin-left: auto;
        font-size: 0.92rem;
        line-height: 1.5;
        box-shadow: 0 2px 12px rgba(99,102,241,0.25);
    }
    .chat-ai {
        background: var(--card);
        border: 1px solid rgba(255,255,255,0.08);
        color: var(--text);
        padding: 14px 18px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 0;
        max-width: 80%;
        font-size: 0.92rem;
        line-height: 1.5;
        box-shadow: 0 2px 12px rgba(0,0,0,0.15);
    }

    /* ——— Eval card ——— */
    .eval-card {
        background: var(--card);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: var(--radius);
        padding: 24px;
        margin-top: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }

    /* ——— Section heading ——— */
    .section-heading {
        font-size: 1.6rem;
        font-weight: 800;
        color: var(--text);
        margin-bottom: 6px;
        letter-spacing: -0.5px;
    }
    .section-sub {
        font-size: 0.95rem;
        color: var(--text-dim);
        margin-bottom: 24px;
    }

    /* ——— Progress bar override ——— */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--accent), var(--accent-light)) !important;
        border-radius: 10px;
    }
    .stProgress > div > div > div {
        background: rgba(255,255,255,0.06) !important;
        border-radius: 10px;
    }

    /* ——— Streamlit native metric override ——— */
    div[data-testid="stMetric"] {
        background: var(--card);
        border: 1px solid rgba(255,255,255,0.06);
        padding: 16px;
        border-radius: var(--radius);
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    }

    /* ——— Big score ——— */
    .big-score {
        font-size: 5rem;
        font-weight: 900;
        background: linear-gradient(135deg, var(--accent), var(--accent-light), #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 16px 0 8px;
        line-height: 1;
    }
    .big-score-label {
        text-align: center;
        color: var(--text-dim);
        font-size: 1rem;
        font-weight: 500;
        margin-bottom: 24px;
    }

    /* ——— Strength / Weakness cards ——— */
    .strength-card {
        background: linear-gradient(135deg, rgba(34,197,94,0.1), rgba(34,197,94,0.03));
        border: 1px solid rgba(34,197,94,0.2);
        border-radius: var(--radius);
        padding: 20px;
    }
    .weakness-card {
        background: linear-gradient(135deg, rgba(239,68,68,0.1), rgba(239,68,68,0.03));
        border: 1px solid rgba(239,68,68,0.2);
        border-radius: var(--radius);
        padding: 20px;
    }

    /* ——— Button override ——— */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="stBaseButton-primary"] {
        background: linear-gradient(135deg, var(--accent), #7c3aed) !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        padding: 10px 28px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.3px !important;
        box-shadow: 0 4px 14px rgba(99,102,241,0.35) !important;
        transition: all 0.25s ease !important;
    }
    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="stBaseButton-primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(99,102,241,0.5) !important;
    }

    /* ——— File uploader ——— */
    [data-testid="stFileUploader"] {
        background: var(--card);
        border: 2px dashed rgba(99,102,241,0.3);
        border-radius: var(--radius);
        padding: 24px;
    }

    /* ——— Text area ——— */
    .stTextArea textarea {
        background: var(--card) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text) !important;
        font-family: 'Inter', sans-serif !important;
    }
    .stTextArea textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px rgba(99,102,241,0.2) !important;
    }

    /* ——— Checkbox override ——— */
    .stCheckbox label span {
        font-size: 0.9rem !important;
    }

    /* ——— Weak area highlight ——— */
    .weak-area {
        background: linear-gradient(135deg, rgba(239,68,68,0.1), rgba(239,68,68,0.03));
        border: 1px solid rgba(239,68,68,0.15);
        border-left: 3px solid var(--danger);
        border-radius: var(--radius-sm);
        padding: 14px 18px;
        margin: 6px 0;
        font-size: 0.9rem;
        color: var(--text);
    }

    /* ——— Fix expander ——— */
    .streamlit-expanderHeader {
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }

    /* ——— Divider ——— */
    .divider {
        height: 1px;
        background: rgba(255,255,255,0.06);
        margin: 24px 0;
    }

    /* ——— Auth form styling ——— */
    .auth-header {
        text-align: center;
        margin-bottom: 24px;
    }
    .auth-header h2 {
        font-size: 1.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff, var(--accent-light));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 6px;
    }
    .auth-header p {
        color: var(--text-dim);
        font-size: 0.9rem;
        margin: 0;
    }
    </style>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------
# SESSION STATE INIT
# -----------------------------------------------------------------
def init_state():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "username" not in st.session_state:
        st.session_state.username = None
    if "full_name" not in st.session_state:
        st.session_state.full_name = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "interview_started" not in st.session_state:
        st.session_state.interview_started = False
    if "interview_feedback" not in st.session_state:
        st.session_state.interview_feedback = None
    if "resume_analyzed" not in st.session_state:
        st.session_state.resume_analyzed = False


def load_user_data():
    """Load user-specific data from database after login."""
    user_id = st.session_state.user_id
    saved_chats = db.get_chat_history(user_id)
    if saved_chats:
        st.session_state.chat_history = [
            {"role": msg["role"], "content": msg["content"]} for msg in saved_chats
        ]
    else:
        welcome_msg = f"Hello {st.session_state.full_name or 'there'}! I'm your AI Career Coach. I can help with interview prep, resume advice, DSA strategies, and career planning. What would you like to work on today?"
        st.session_state.chat_history = [
            {"role": "ai", "content": welcome_msg}
        ]
        db.save_chat_message(user_id, "ai", welcome_msg)


# -----------------------------------------------------------------
# HELPER — render a styled card via HTML
# -----------------------------------------------------------------
def card(content: str, extra_class: str = ""):
    st.markdown(
        f'<div class="card {extra_class}">{content}</div>',
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str, delta: str = ""):
    delta_html = f'<div class="metric-delta">{delta}</div>' if delta else ""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------
# 1. 🏠 DASHBOARD
# -----------------------------------------------------------------
def render_dashboard():
    # Fetch stats from database
    stats = db.get_dashboard_stats(st.session_state.user_id)
    placement_score = stats["placement_score"] or 62
    dsa_score = stats["dsa_score"] or 50
    aptitude_score = stats["aptitude_score"] or 75
    streak = stats["streak"] or 0

    # Determine DSA level from score
    if dsa_score >= 80:
        dsa_level = "Advanced"
    elif dsa_score >= 50:
        dsa_level = "Intermediate"
    else:
        dsa_level = "Beginner"

    # Hero
    st.markdown(
        """
        <div class="hero">
            <h1>Your AI Career Coach</h1>
            <p>Personalized guidance. Real results.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Smart alert at top
    st.markdown(
        """
        <div class="smart-alert">
            ⚠️ <strong>Stay consistent!</strong> Keep your streak going to hit your 80% placement target.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Placement Score", f"{placement_score}%", "↑ Track your growth")
    with col2:
        metric_card("DSA Level", dsa_level, f"Score: {dsa_score}%")
    with col3:
        metric_card("Aptitude", f"{aptitude_score}%", "")
    with col4:
        metric_card("Consistency", f"{streak} Days", "🔥 Streak" if streak > 0 else "Start today!")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Placement progress + AI Insight
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown('<div class="section-heading">Placement Readiness</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Your progress toward placement-ready status</div>', unsafe_allow_html=True)
        st.progress(placement_score / 100)
        st.caption(f"{placement_score} / 100  —  Target: 80%")

    with col_right:
        st.markdown(
            f"""
            <div class="ai-insight">
                <h4>🧠 AI Insight</h4>
                <p>Your placement probability is <strong>{placement_score}%</strong>. Focus on DSA Hard problems and take 2 mock interviews this week to push toward <strong>80%</strong>.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# -----------------------------------------------------------------
# 2. 📄 RESUME ANALYZER
# -----------------------------------------------------------------
def render_resume_analyzer():
    st.markdown('<div class="section-heading">Resume Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Upload your resume for instant AI-driven feedback</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Resume (PDF / TXT)", type=["pdf", "txt"])

    if st.button("🚀  Analyze Resume", type="primary"):
        if uploaded_file is None:
            st.warning("Please upload a file first.")
        else:
            with st.spinner("Analyzing resume against industry standards…"):
                time.sleep(2)

            st.session_state.resume_analyzed = True

    if st.session_state.resume_analyzed:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # Skills
        st.markdown('<div class="section-heading" style="font-size:1.2rem">Extracted Skills</div>', unsafe_allow_html=True)
        skills = ["Python", "JavaScript", "React", "Node.js", "HTML/CSS", "SQL", "Git", "REST APIs"]
        tags = "".join([f'<span class="skill-tag">{s}</span>' for s in skills])
        st.markdown(tags, unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                """
                <div class="strength-card">
                    <h4 style="color:#22c55e; margin-top:0;">✅ Strengths</h4>
                    <ul style="margin:0; padding-left:18px; color:#cbd5e1; line-height:1.8;">
                        <li>Strong web development foundation</li>
                        <li>Multiple personal projects</li>
                        <li>Clean formatting & readability</li>
                        <li>Relevant tech stack for SDE roles</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                """
                <div class="weakness-card">
                    <h4 style="color:#ef4444; margin-top:0;">⚠️ Weaknesses</h4>
                    <ul style="margin:0; padding-left:18px; color:#cbd5e1; line-height:1.8;">
                        <li>No cloud technologies (AWS/GCP)</li>
                        <li>Missing quantifiable metrics</li>
                        <li>No Docker / containerization</li>
                        <li>System Design not mentioned</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("")
        st.markdown(
            """
            <div class="ai-insight">
                <h4>🚨 Missing Skills for SDE Goal</h4>
                <p>Add <strong>AWS/GCP</strong>, <strong>Docker</strong>, and <strong>System Design</strong> experience to significantly boost your resume score.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# -----------------------------------------------------------------
# 3. 📊 PLACEMENT PREDICTOR
# -----------------------------------------------------------------
def render_placement_predictor():
    st.markdown('<div class="section-heading">Placement Predictor</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">AI-powered prediction of your placement readiness</div>', unsafe_allow_html=True)

    with st.spinner("Calculating placement score…"):
        time.sleep(1)

    st.markdown('<div class="big-score">62%</div>', unsafe_allow_html=True)
    st.markdown('<div class="big-score-label">Placement Readiness Score</div>', unsafe_allow_html=True)

    st.progress(0.62)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        card(
            """
            <h4 style="color:#f1f5f9; margin-top:0;">📋 Score Breakdown</h4>
            <ul style="margin:0; padding-left:18px; color:#94a3b8; line-height:2;">
                <li><strong style="color:#22c55e;">High Aptitude</strong> — Logical reasoning boosts your score</li>
                <li><strong style="color:#f59e0b;">Low Mock Interviews</strong> — Behavioral confidence needs work</li>
                <li><strong style="color:#ef4444;">Resume Gap</strong> — Missing cloud & DevOps experience</li>
            </ul>
            """
        )
    with col2:
        card(
            """
            <h4 style="color:#f1f5f9; margin-top:0;">💡 Improvement Suggestions</h4>
            <ul style="margin:0; padding-left:18px; color:#94a3b8; line-height:2;">
                <li>Solve 5 Hard-level DSA problems this week <span class="badge-hard">+4%</span></li>
                <li>Take 2 mock interviews <span class="badge-medium">+3%</span></li>
                <li>Add System Design basics to resume <span class="badge-easy">+2%</span></li>
                <li>Dockerize one project <span class="badge-medium">+2%</span></li>
            </ul>
            """
        )


# -----------------------------------------------------------------
# 4. 🧠 ADAPTIVE LEARNING PATH
# -----------------------------------------------------------------
def render_adaptive_learning():
    st.markdown('<div class="section-heading">Adaptive Learning Path</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Your personalized 7-day sprint to patch weak areas</div>', unsafe_allow_html=True)

    days = [
        {"day": "Day 1 — Today", "focus": "System Design Basics", "tasks": ["Read 'Grokking System Design' Ch 1", "Draw a URL Shortener architecture"], "diff": "Medium"},
        {"day": "Day 2", "focus": "DSA — Trees", "tasks": ["LC #104  Maximum Depth of Binary Tree", "LC #236  LCA of a Binary Tree"], "diff": "Hard"},
        {"day": "Day 3", "focus": "Mock Interview Prep", "tasks": ["Record a 2-min self introduction", "Review STAR method for behavioral Q's"], "diff": "Easy"},
        {"day": "Day 4", "focus": "Cloud Deployment", "tasks": ["Dockerize your React app", "Deploy to AWS EC2 or Vercel"], "diff": "Medium"},
        {"day": "Day 5", "focus": "DSA — Graphs", "tasks": ["LC #200  Number of Islands", "Review BFS/DFS templates"], "diff": "Hard"},
        {"day": "Day 6", "focus": "Resume Update", "tasks": ["Add quantifiable metrics to bullet points", "Re-run Resume Analyzer"], "diff": "Easy"},
        {"day": "Day 7", "focus": "Rest & Review", "tasks": ["Review all mistakes from Day 1–6", "Plan next week's sprint"], "diff": "Easy"},
    ]

    for i, d in enumerate(days):
        diff = d["diff"]
        badge_class = {"Easy": "badge-easy", "Medium": "badge-medium", "Hard": "badge-hard"}[diff]

        st.markdown(
            f"""
            <div class="day-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div class="day-title">{d['day']}</div>
                    <span class="{badge_class}">{diff}</span>
                </div>
                <div class="day-focus">{d['focus']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        for task in d["tasks"]:
            st.checkbox(task, key=f"learn_{i}_{task}")


# -----------------------------------------------------------------
# 5. 🤖 AI MENTOR CHAT
# -----------------------------------------------------------------
def render_ai_mentor():
    st.markdown('<div class="section-heading">AI Mentor</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Chat with your career coach for advice, tips, and strategies</div>', unsafe_allow_html=True)

    # Render chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-user">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-ai">🤖  {msg["content"]}</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Input
    if prompt := st.chat_input("Ask me anything — interview tips, DSA help, career advice…"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        db.save_chat_message(st.session_state.user_id, "user", prompt)  # Save to DB

        # Mock AI responses
        responses = [
            "Great question! For optimizing search algorithms, consider using a Hash Map for O(1) lookups, or a Binary Search Tree for O(log N) ordered operations. Would you like me to walk through a specific example?",
            "I recommend focusing on the STAR method for behavioral interviews: Situation, Task, Action, Result. This framework helps structure your answers clearly.",
            "For system design interviews, start with requirements clarification, then high-level design, then deep dive. Practice with classic problems like 'Design a URL Shortener' or 'Design Twitter'.",
            "To improve your DSA skills, I suggest the 'Blind 75' list. Start with Easy problems, then progress to Medium. Focus on understanding patterns, not memorizing solutions.",
            "For your resume, quantify your achievements. Instead of 'Improved performance', write 'Reduced API latency by 40% through query optimization'. Numbers make a huge difference.",
        ]
        reply = random.choice(responses)
        st.session_state.chat_history.append({"role": "ai", "content": reply})
        db.save_chat_message(st.session_state.user_id, "ai", reply)  # Save to DB
        st.rerun()


# -----------------------------------------------------------------
# 6. 🎤 MOCK INTERVIEW
# -----------------------------------------------------------------
def render_mock_interview():
    st.markdown('<div class="section-heading">Mock Interview</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Practice with AI-generated interview questions</div>', unsafe_allow_html=True)

    if not st.session_state.interview_started:
        card(
            """
            <div style="text-align:center; padding:20px 0;">
                <div style="font-size:3rem; margin-bottom:12px;">🎤</div>
                <h3 style="color:#f1f5f9; margin:0 0 8px;">Ready to practice?</h3>
                <p style="color:#94a3b8; margin:0;">The AI will ask you a technical question and evaluate your answer on correctness, clarity, and depth.</p>
            </div>
            """
        )
        if st.button("▶️  Start Interview", type="primary"):
            st.session_state.interview_started = True
            st.session_state.interview_feedback = None
            st.rerun()
    else:
        st.markdown(
            """
            <div class="card">
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px;">
                    <span style="font-size:1.2rem;">🤖</span>
                    <span style="color:#94a3b8; font-size:0.85rem; font-weight:600; text-transform:uppercase; letter-spacing:0.5px;">Interviewer</span>
                </div>
                <p style="color:#f1f5f9; font-size:1.05rem; margin:0; line-height:1.7;">
                    Explain the difference between <code style="background:rgba(99,102,241,0.2); padding:2px 6px; border-radius:4px;">let</code>,
                    <code style="background:rgba(99,102,241,0.2); padding:2px 6px; border-radius:4px;">var</code>, and
                    <code style="background:rgba(99,102,241,0.2); padding:2px 6px; border-radius:4px;">const</code> in JavaScript. When would you use each?
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        answer = st.text_area("Your Answer:", height=150, placeholder="Type your response here…")

        col1, col2, _ = st.columns([1, 1, 3])
        with col1:
            if st.button("Submit Answer", type="primary"):
                if answer.strip():
                    with st.spinner("Evaluating your response…"):
                        time.sleep(1.5)
                    feedback_data = {
                        "correctness": "85%",
                        "clarity": "70%",
                        "depth": "75%",
                        "feedback": "Good understanding of block vs function scope. However, you didn't mention that `const` arrays and objects can still be mutated (only the reference is immutable). Default to `const` unless reassignment is needed.",
                    }
                    st.session_state.interview_feedback = feedback_data

                    # Save interview score to database
                    question = "Explain the difference between let, var, and const in JavaScript."
                    db.save_interview_score(
                        st.session_state.user_id,
                        question=question,
                        answer=answer.strip(),
                        correctness=85,
                        clarity=70,
                        depth=75,
                        feedback=feedback_data["feedback"]
                    )
                    st.rerun()
                else:
                    st.warning("Please write an answer before submitting.")
        with col2:
            if st.button("End Interview"):
                st.session_state.interview_started = False
                st.session_state.interview_feedback = None
                st.rerun()

        if st.session_state.interview_feedback:
            fb = st.session_state.interview_feedback
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="eval-card">
                    <h4 style="color:#f1f5f9; margin-top:0; margin-bottom:16px;">📊 Evaluation</h4>
                    <div style="display:flex; gap:20px; margin-bottom:16px;">
                        <div class="metric-card" style="flex:1;">
                            <div class="metric-label">Correctness</div>
                            <div class="metric-value">{fb['correctness']}</div>
                        </div>
                        <div class="metric-card" style="flex:1;">
                            <div class="metric-label">Clarity</div>
                            <div class="metric-value">{fb['clarity']}</div>
                        </div>
                        <div class="metric-card" style="flex:1;">
                            <div class="metric-label">Depth</div>
                            <div class="metric-value">{fb['depth']}</div>
                        </div>
                    </div>
                    <div style="background:rgba(99,102,241,0.08); border:1px solid rgba(99,102,241,0.2); border-radius:10px; padding:16px;">
                        <strong style="color:#818cf8;">💬 Feedback:</strong>
                        <p style="color:#cbd5e1; margin:8px 0 0; line-height:1.6;">{fb['feedback']}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# -----------------------------------------------------------------
# 7. 📉 PROGRESS TRACKING
# -----------------------------------------------------------------
def render_progress_tracking():
    st.markdown('<div class="section-heading">Progress Tracking</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Monitor your skill growth and task completion</div>', unsafe_allow_html=True)

    # Skill growth line chart
    st.markdown("#### 📈 Skill Growth — Last 30 Days")
    dates = pd.date_range(end=datetime.date.today(), periods=30)
    chart_data = pd.DataFrame(
        {
            "DSA": [40 + (i * 1.2) + (i % 3) for i in range(30)],
            "Aptitude": [50 + (i * 0.8) - (i % 2) for i in range(30)],
        },
        index=dates,
    )
    st.line_chart(chart_data, color=["#6366f1", "#22c55e"])

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Task completion bar chart
    st.markdown("#### 📊 Weekly Task Completion")
    bar_data = pd.DataFrame(
        {
            "Completed": [12, 15, 10, 18],
            "Missed": [3, 1, 5, 2],
        },
        index=["Week 1", "Week 2", "Week 3", "Week 4"],
    )
    st.bar_chart(bar_data, color=["#6366f1", "#ef4444"])

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Weak areas
    st.markdown("#### ⚠️ Areas Needing Attention")
    weak = [
        ("Mock Interviews", "Only 2 completed — target is 6 per month"),
        ("System Design", "No study sessions logged in 2 weeks"),
        ("Consistency", "3 days missed in the last sprint"),
    ]
    for area, detail in weak:
        st.markdown(
            f"""
            <div class="weak-area">
                <strong>{area}:</strong> {detail}
            </div>
            """,
            unsafe_allow_html=True,
        )


# -----------------------------------------------------------------
# NAVBAR (for authenticated users)
# -----------------------------------------------------------------
def render_authenticated_navbar():
    """Render the top navigation bar for authenticated users."""
    name = st.session_state.full_name or st.session_state.username or "U"
    initials = "".join([w[0].upper() for w in name.split()[:2]])

    st.markdown(
        f"""
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 14px 28px;
            background: rgba(17, 24, 39, 0.85);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 16px;
            margin-bottom: 20px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.25);
        ">
            <div style="display:flex; align-items:center; gap:12px;">
                <div style="
                    width:38px; height:38px; border-radius:10px;
                    background:linear-gradient(135deg, #6366f1, #7c3aed);
                    display:flex; align-items:center; justify-content:center;
                    font-size:1.2rem; font-weight:800; color:white;
                    box-shadow:0 2px 10px rgba(99,102,241,0.35);
                ">CF</div>
                <div style="
                    font-size:1.35rem; font-weight:800;
                    background:linear-gradient(135deg, #fff, #818cf8);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    letter-spacing:-0.5px;
                ">CareerForge</div>
            </div>
            <div style="display:flex; align-items:center; gap:10px;">
                <span style="color:#f1f5f9; font-size:0.9rem; font-weight:500;">{st.session_state.full_name or st.session_state.username}</span>
                <div style="
                    width:34px; height:34px; border-radius:50%;
                    background:linear-gradient(135deg, #6366f1, #a78bfa);
                    display:flex; align-items:center; justify-content:center;
                    font-size:0.85rem; font-weight:700; color:white;
                ">{initials}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # Logout button (small, right-aligned)
    cols = st.columns([10, 1])
    with cols[1]:
        if st.button("Logout", key="logout_btn"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


# -----------------------------------------------------------------
# AUTH DIALOGS — Sign In / Sign Up as separate pages
# -----------------------------------------------------------------
def render_signin_page():
    """Render the Sign In page."""
    st.markdown(
        """
        <div class="hero" style="padding-bottom:10px;">
            <h1>Welcome Back</h1>
            <p>Sign in to continue your career journey</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, col_form, _ = st.columns([1.5, 2, 1.5])

    with col_form:
        st.markdown(
            """
            <div class="auth-header">
                <h2>Sign In</h2>
                <p>Enter your credentials</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("signin_form", clear_on_submit=False):
            si_username = st.text_input("Username", key="si_user", placeholder="Enter your username")
            si_password = st.text_input("Password", type="password", key="si_pass", placeholder="Enter your password")
            si_submit = st.form_submit_button("Sign In", type="primary", use_container_width=True)

            if si_submit:
                if not si_username or not si_password:
                    st.error("Please fill in all fields.")
                else:
                    user = db.authenticate_user(si_username.strip(), si_password)
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.user_id = user["id"]
                        st.session_state.username = user["username"]
                        st.session_state.full_name = user["full_name"]
                        st.session_state.show_page = "dashboard"
                        load_user_data()
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")

        st.markdown("")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("← Back to Home", use_container_width=True):
                st.session_state.show_page = "landing"
                st.rerun()
        with col_b:
            if st.button("Create Account →", use_container_width=True):
                st.session_state.show_page = "signup"
                st.rerun()


def render_signup_page():
    """Render the Sign Up page."""
    st.markdown(
        """
        <div class="hero" style="padding-bottom:10px;">
            <h1>Join CareerForge</h1>
            <p>Create your free account and start your journey</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, col_form, _ = st.columns([1.5, 2, 1.5])

    with col_form:
        st.markdown(
            """
            <div class="auth-header">
                <h2>Sign Up</h2>
                <p>It only takes a minute</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("signup_form", clear_on_submit=True):
            su_fullname = st.text_input("Full Name", key="su_name", placeholder="Enter your full name")
            su_email = st.text_input("Email", key="su_email", placeholder="Enter your email")
            su_username = st.text_input("Username", key="su_user", placeholder="Choose a username")
            su_password = st.text_input("Password", type="password", key="su_pass", placeholder="Create a password")
            su_submit = st.form_submit_button("Create Account", type="primary", use_container_width=True)

            if su_submit:
                if not su_fullname or not su_username or not su_password or not su_email:
                    st.error("Please fill in all fields.")
                elif len(su_password) < 4:
                    st.error("Password must be at least 4 characters.")
                elif db.check_username_exists(su_username.strip()):
                    st.error("Username already taken. Try another one.")
                else:
                    user_id = db.create_user(
                        username=su_username.strip(),
                        full_name=su_fullname.strip(),
                        email=su_email.strip(),
                        password=su_password,
                    )
                    if user_id:
                        st.session_state.authenticated = True
                        st.session_state.user_id = user_id
                        st.session_state.username = su_username.strip()
                        st.session_state.full_name = su_fullname.strip()
                        st.session_state.show_page = "dashboard"
                        load_user_data()
                        st.success("Account created! Redirecting...")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Username or email already exists.")

        st.markdown("")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("← Back to Home", key="back_home_su", use_container_width=True):
                st.session_state.show_page = "landing"
                st.rerun()
        with col_b:
            if st.button("Already have an account? Sign In →", key="goto_signin", use_container_width=True):
                st.session_state.show_page = "signin"
                st.rerun()


# -----------------------------------------------------------------
# LANDING PAGE — shown to unauthenticated / first-time visitors
# -----------------------------------------------------------------
def render_landing_page():
    """Immersive landing page with sparkle cursor, animated background, and interactive features."""

    # ==========================================
    # FULL-PAGE INTERACTIVE EXPERIENCE VIA HTML
    # Write HTML to a static file so we can serve it
    # via an unsandboxed iframe (allows navigation)
    # ==========================================
    import os
    
    # Create static directory for Streamlit
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    os.makedirs(static_dir, exist_ok=True)
    
    html_content = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');

* { margin:0; padding:0; box-sizing:border-box; }

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: #0a0e1a;
    color: #f1f5f9;
    overflow-x: hidden;
    cursor: none;
}

/* ——— Custom Cursor ——— */
.cursor-dot {
    width: 10px; height: 10px;
    background: radial-gradient(circle, #fff 0%, #818cf8 60%, transparent 100%);
    border-radius: 50%;
    position: fixed;
    pointer-events: none;
    z-index: 99999;
    transition: transform 0.05s ease;
    box-shadow: 0 0 20px rgba(129,140,248,0.8), 0 0 40px rgba(99,102,241,0.4), 0 0 6px #fff;
}
.cursor-ring {
    width: 40px; height: 40px;
    border: 2px solid rgba(129,140,248,0.5);
    border-radius: 50%;
    position: fixed;
    pointer-events: none;
    z-index: 99998;
    transition: width 0.15s ease, height 0.15s ease, border-color 0.15s ease;
    box-shadow: 0 0 12px rgba(129,140,248,0.15);
}

/* ——— Interactive Background Glow (follows cursor) ——— */
.cursor-glow {
    position: fixed;
    width: 600px; height: 600px;
    border-radius: 50%;
    pointer-events: none;
    z-index: 2;
    background: radial-gradient(circle, rgba(99,102,241,0.12) 0%, rgba(124,58,237,0.06) 30%, transparent 70%);
    filter: blur(40px);
    transform: translate(-50%, -50%);
    transition: none;
}

/* ——— Sparkle particles (cross/star shaped) ——— */
.sparkle {
    position: fixed;
    pointer-events: none;
    z-index: 99997;
    animation: sparkle-fade 1s ease forwards;
}
.sparkle::before, .sparkle::after {
    content: '';
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    background: inherit;
    border-radius: 1px;
}
.sparkle::before {
    width: 100%; height: 30%;
}
.sparkle::after {
    width: 30%; height: 100%;
}
@keyframes sparkle-fade {
    0% { transform: scale(1) rotate(0deg) translate(0,0); opacity:1; }
    50% { transform: scale(1.3) rotate(45deg) translate(calc(var(--tx) * 0.5), calc(var(--ty) * 0.5)); opacity:0.7; }
    100% { transform: scale(0) rotate(90deg) translate(var(--tx), var(--ty)); opacity:0; }
}

/* ——— Loading Screen ——— */
.loading-screen {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: #0a0e1a;
    z-index: 100000;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    transition: opacity 0.6s ease, visibility 0.6s ease;
}
.loading-screen.hidden {
    opacity: 0;
    visibility: hidden;
}
.loading-logo {
    width: 80px; height: 80px;
    border-radius: 20px;
    background: linear-gradient(135deg, #6366f1, #7c3aed);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    font-weight: 900;
    color: white;
    animation: pulse-glow 1.5s ease-in-out infinite;
    box-shadow: 0 0 40px rgba(99,102,241,0.4);
}
@keyframes pulse-glow {
    0%, 100% { transform: scale(1); box-shadow: 0 0 40px rgba(99,102,241,0.4); }
    50% { transform: scale(1.08); box-shadow: 0 0 60px rgba(99,102,241,0.6); }
}
.loading-bar-track {
    width: 200px; height: 4px;
    background: rgba(255,255,255,0.08);
    border-radius: 10px;
    margin-top: 28px;
    overflow: hidden;
}
.loading-bar-fill {
    height: 100%;
    border-radius: 10px;
    background: linear-gradient(90deg, #6366f1, #818cf8, #a78bfa);
    animation: load-progress 1.8s ease-in-out forwards;
}
@keyframes load-progress {
    0% { width: 0%; }
    100% { width: 100%; }
}
.loading-text {
    margin-top: 16px;
    font-size: 0.85rem;
    color: #64748b;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-weight: 600;
}

/* ——— Animated Background ——— */
.bg-canvas {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: 0;
    overflow: hidden;
}
.bg-orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    animation: float-orb 20s ease-in-out infinite;
    opacity: 0.4;
    transition: transform 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
.bg-orb:nth-child(1) {
    width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(99,102,241,0.35), transparent);
    top: -10%; left: -5%;
    animation-duration: 25s;
}
.bg-orb:nth-child(2) {
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(124,58,237,0.3), transparent);
    bottom: -10%; right: -5%;
    animation-duration: 20s;
    animation-delay: -5s;
}
.bg-orb:nth-child(3) {
    width: 350px; height: 350px;
    background: radial-gradient(circle, rgba(6,182,212,0.2), transparent);
    top: 40%; left: 50%;
    animation-duration: 30s;
    animation-delay: -10s;
}
.bg-orb:nth-child(4) {
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(244,63,94,0.15), transparent);
    top: 20%; right: 20%;
    animation-duration: 22s;
    animation-delay: -7s;
}
@keyframes float-orb {
    0%, 100% { transform: translate(0, 0) scale(1); }
    25% { transform: translate(60px, -40px) scale(1.1); }
    50% { transform: translate(-30px, 60px) scale(0.95); }
    75% { transform: translate(40px, 30px) scale(1.05); }
}

/* ——— Grid lines (deforms near cursor) ——— */
.grid-overlay {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: 1;
    background-image:
        linear-gradient(rgba(99,102,241,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,102,241,0.03) 1px, transparent 1px);
    background-size: 60px 60px;
    pointer-events: none;
    transition: background-position 0.3s ease;
}

/* ——— Main Content ——— */
.main-content {
    position: relative;
    z-index: 10;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 24px;
}

/* ——— Top Bar — CareerForge logo + Nav + Auth ——— */
.top-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 0;
    gap: 20px;
}
.brand-link {
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
    text-decoration: none;
    flex-shrink: 0;
    transition: transform 0.2s ease;
}
.brand-link:hover {
    transform: scale(1.03);
}
.brand-logo {
    width: 42px; height: 42px;
    border-radius: 12px;
    background: linear-gradient(135deg, #6366f1, #7c3aed);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    font-weight: 900;
    color: white;
    box-shadow: 0 4px 16px rgba(99,102,241,0.4);
    transition: box-shadow 0.3s ease;
}
.brand-link:hover .brand-logo {
    box-shadow: 0 6px 24px rgba(99,102,241,0.6);
}
.brand-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #fff, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
}

/* ——— Center Nav ——— */
.nav-center {
    display: flex;
    align-items: center;
    gap: 4px;
    background: rgba(17, 24, 39, 0.7);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 5px 6px;
}
.nav-link {
    padding: 9px 18px;
    font-size: 0.85rem;
    font-weight: 500;
    color: #94a3b8;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.25s ease;
    text-decoration: none;
    white-space: nowrap;
    position: relative;
    overflow: hidden;
}
.nav-link:hover {
    color: #f1f5f9;
    background: rgba(99,102,241,0.12);
}
.nav-link::after {
    content: '';
    position: absolute;
    bottom: 4px; left: 50%;
    width: 0; height: 2px;
    background: #6366f1;
    border-radius: 2px;
    transition: all 0.3s ease;
    transform: translateX(-50%);
}
.nav-link:hover::after {
    width: 60%;
}

/* ——— Auth Buttons ——— */
.auth-btns {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-shrink: 0;
}
.btn-signin {
    padding: 9px 22px;
    font-size: 0.85rem;
    font-weight: 600;
    color: #cbd5e1;
    background: transparent;
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.25s ease;
}
.btn-signin:hover {
    color: #fff;
    border-color: rgba(99,102,241,0.5);
    background: rgba(99,102,241,0.08);
    transform: translateY(-1px);
}
.btn-signup {
    padding: 9px 22px;
    font-size: 0.85rem;
    font-weight: 600;
    color: white;
    background: linear-gradient(135deg, #6366f1, #7c3aed);
    border: none;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.25s ease;
    box-shadow: 0 4px 14px rgba(99,102,241,0.35);
}
.btn-signup:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 22px rgba(99,102,241,0.5);
}

/* ——— HERO ——— */
.hero-section {
    text-align: center;
    padding: 80px 20px 60px;
    position: relative;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 18px;
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 50px;
    font-size: 0.82rem;
    font-weight: 600;
    color: #818cf8;
    margin-bottom: 28px;
    animation: fade-in-up 0.8s ease;
}
.hero-badge .pulse-dot {
    width: 8px; height: 8px;
    background: #22c55e;
    border-radius: 50%;
    animation: pulse-dot 2s ease-in-out infinite;
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(1.5); }
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 4.5rem;
    font-weight: 700;
    line-height: 1.08;
    letter-spacing: -2.5px;
    margin-bottom: 24px;
    animation: fade-in-up 0.8s ease 0.1s both;
}
.hero-title .line1 {
    display: block;
    color: #f1f5f9;
}
.hero-title .line2 {
    display: block;
    background: linear-gradient(135deg, #6366f1, #818cf8, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-title .line3 {
    display: block;
    background: linear-gradient(135deg, #06b6d4 0%, #818cf8 50%, #f43f5e 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-subtitle {
    font-size: 1.2rem;
    color: #94a3b8;
    max-width: 580px;
    margin: 0 auto 40px;
    line-height: 1.7;
    animation: fade-in-up 0.8s ease 0.2s both;
}
@keyframes fade-in-up {
    0% { opacity: 0; transform: translateY(30px); }
    100% { opacity: 1; transform: translateY(0); }
}

/* ——— Hero CTAs ——— */
.hero-ctas {
    display: flex;
    justify-content: center;
    gap: 16px;
    animation: fade-in-up 0.8s ease 0.3s both;
}
.cta-primary {
    padding: 16px 36px;
    font-size: 1rem;
    font-weight: 700;
    color: white;
    background: linear-gradient(135deg, #6366f1, #7c3aed);
    border: none;
    border-radius: 14px;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 6px 24px rgba(99,102,241,0.4);
    position: relative;
    overflow: hidden;
}
.cta-primary:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 36px rgba(99,102,241,0.55);
}
.cta-primary::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
    transition: 0.6s ease;
}
.cta-primary:hover::before {
    left: 100%;
}
.cta-secondary {
    padding: 16px 36px;
    font-size: 1rem;
    font-weight: 600;
    color: #cbd5e1;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 14px;
    cursor: pointer;
    transition: all 0.3s ease;
}
.cta-secondary:hover {
    color: #fff;
    border-color: rgba(99,102,241,0.5);
    background: rgba(99,102,241,0.08);
    transform: translateY(-3px);
}

/* ——— Floating collab badges (Real-Time Collaborative Animation) ——— */
.collab-avatars {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0;
    margin-top: 48px;
    animation: fade-in-up 0.8s ease 0.5s both;
}
.collab-avatar {
    width: 40px; height: 40px;
    border-radius: 50%;
    border: 3px solid #0a0e1a;
    margin-left: -10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 700;
    color: white;
    animation: avatar-pop 0.5s ease both;
    position: relative;
}
.collab-avatar:nth-child(1) { background: #6366f1; animation-delay: 0.6s; margin-left: 0; }
.collab-avatar:nth-child(2) { background: #22c55e; animation-delay: 0.7s; }
.collab-avatar:nth-child(3) { background: #f59e0b; animation-delay: 0.8s; }
.collab-avatar:nth-child(4) { background: #f43f5e; animation-delay: 0.9s; }
.collab-avatar:nth-child(5) { background: #06b6d4; animation-delay: 1.0s; }
@keyframes avatar-pop {
    0% { transform: scale(0) rotate(-20deg); opacity: 0; }
    100% { transform: scale(1) rotate(0); opacity: 1; }
}
.collab-text {
    margin-left: 14px;
    font-size: 0.88rem;
    color: #94a3b8;
    animation: fade-in-up 0.8s ease 1.1s both;
}
.collab-text strong { color: #22c55e; }

/* ——— Live typing indicator ——— */
.typing-indicator {
    display: inline-flex; gap: 4px;
    margin-left: 8px;
}
.typing-indicator span {
    width: 5px; height: 5px;
    background: #22c55e;
    border-radius: 50%;
    animation: typing-bounce 1.4s ease-in-out infinite;
}
.typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
.typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
@keyframes typing-bounce {
    0%, 60%, 100% { transform: translateY(0); }
    30% { transform: translateY(-6px); }
}

/* ——— FEATURES SECTION ——— */
.section-title-area {
    text-align: center;
    margin-bottom: 48px;
}
.section-tag {
    display: inline-block;
    padding: 6px 16px;
    background: rgba(99,102,241,0.1);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 50px;
    font-size: 0.78rem;
    font-weight: 700;
    color: #818cf8;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 16px;
}
.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.8rem;
    font-weight: 700;
    color: #f1f5f9;
    letter-spacing: -1px;
    margin-bottom: 12px;
}
.section-desc {
    font-size: 1.1rem;
    color: #94a3b8;
    max-width: 550px;
    margin: 0 auto;
}

/* ——— Feature Grid ——— */
.features-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-bottom: 100px;
}
.feature-card {
    background: rgba(17, 24, 39, 0.6);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 20px;
    padding: 32px 28px;
    position: relative;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    cursor: pointer;
}
.feature-card:hover {
    transform: translateY(-8px);
    border-color: var(--glow-color, rgba(99,102,241,0.4));
    box-shadow: 0 20px 60px rgba(0,0,0,0.3), 0 0 40px var(--glow-color-dim, rgba(99,102,241,0.1));
}
.feature-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: radial-gradient(600px circle at var(--mouse-x, 50%) var(--mouse-y, 50%), var(--glow-color-dim, rgba(99,102,241,0.06)), transparent 40%);
    opacity: 0;
    transition: opacity 0.4s ease;
}
.feature-card:hover::before {
    opacity: 1;
}
.feature-icon {
    width: 56px; height: 56px;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.6rem;
    margin-bottom: 20px;
    position: relative;
    z-index: 1;
    transition: transform 0.3s ease;
}
.feature-card:hover .feature-icon {
    transform: scale(1.1) rotate(-3deg);
}
.feature-card h3 {
    font-size: 1.15rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 10px;
    position: relative;
    z-index: 1;
}
.feature-card p {
    font-size: 0.9rem;
    color: #94a3b8;
    line-height: 1.65;
    position: relative;
    z-index: 1;
}
.feature-card .feature-arrow {
    position: absolute;
    bottom: 24px; right: 24px;
    width: 32px; height: 32px;
    border-radius: 50%;
    background: rgba(255,255,255,0.04);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
    color: #64748b;
    transition: all 0.3s ease;
    z-index: 1;
}
.feature-card:hover .feature-arrow {
    background: var(--glow-color, rgba(99,102,241,0.3));
    color: white;
    transform: translateX(3px);
}

/* ——— How It Works ——— */
.steps-section {
    margin-bottom: 100px;
}
.steps-row {
    display: flex;
    gap: 0;
    position: relative;
}
.steps-row::before {
    content: '';
    position: absolute;
    top: 50px;
    left: 15%;
    right: 15%;
    height: 2px;
    background: linear-gradient(90deg, rgba(99,102,241,0.3), rgba(124,58,237,0.3), rgba(245,158,11,0.3));
    z-index: 0;
}
.step-item {
    flex: 1;
    text-align: center;
    padding: 0 20px;
    position: relative;
    z-index: 1;
}
.step-num {
    width: 64px; height: 64px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.4rem;
    font-weight: 800;
    color: white;
    margin: 0 auto 20px;
    position: relative;
    transition: transform 0.3s ease;
}
.step-item:hover .step-num {
    transform: scale(1.12);
}
.step-num::after {
    content: '';
    position: absolute;
    width: 80px; height: 80px;
    border-radius: 50%;
    border: 2px dashed rgba(255,255,255,0.08);
    animation: spin-slow 20s linear infinite;
}
@keyframes spin-slow {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
.step-item h3 {
    font-size: 1.1rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 10px;
}
.step-item p {
    font-size: 0.88rem;
    color: #94a3b8;
    line-height: 1.6;
}

/* ——— Stats / Social Proof ——— */
.stats-bar {
    background: linear-gradient(135deg, rgba(99,102,241,0.1), rgba(124,58,237,0.06));
    border: 1px solid rgba(99,102,241,0.15);
    border-radius: 24px;
    padding: 48px 40px;
    display: flex;
    justify-content: space-around;
    align-items: center;
    margin-bottom: 100px;
    position: relative;
    overflow: hidden;
}
.stats-bar::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: conic-gradient(from 0deg, transparent, rgba(99,102,241,0.05), transparent, rgba(124,58,237,0.05), transparent);
    animation: spin-slow 25s linear infinite;
}
.stat-item {
    text-align: center;
    position: relative;
    z-index: 1;
}
.stat-num {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, var(--stat-color-1, #6366f1), var(--stat-color-2, #818cf8));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
    margin-bottom: 8px;
}
.stat-label {
    font-size: 0.82rem;
    color: #94a3b8;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

/* ——— Testimonials ——— */
.testimonials-section {
    margin-bottom: 100px;
}
.testimonials-track {
    display: flex;
    gap: 20px;
    animation: scroll-left 30s linear infinite;
}
.testimonials-track:hover {
    animation-play-state: paused;
}
@keyframes scroll-left {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}
.testimonial-card {
    min-width: 350px;
    background: rgba(17, 24, 39, 0.6);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 20px;
    padding: 28px;
    flex-shrink: 0;
    transition: all 0.3s ease;
}
.testimonial-card:hover {
    border-color: rgba(99,102,241,0.3);
    transform: translateY(-4px);
}
.testimonial-stars {
    color: #f59e0b;
    font-size: 0.9rem;
    margin-bottom: 14px;
    letter-spacing: 2px;
}
.testimonial-text {
    font-size: 0.92rem;
    color: #cbd5e1;
    line-height: 1.7;
    margin-bottom: 18px;
    font-style: italic;
}
.testimonial-author {
    display: flex;
    align-items: center;
    gap: 12px;
}
.testimonial-avatar {
    width: 38px; height: 38px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    font-weight: 700;
    color: white;
}
.testimonial-name {
    font-size: 0.88rem;
    font-weight: 600;
    color: #f1f5f9;
}
.testimonial-role {
    font-size: 0.78rem;
    color: #64748b;
}

/* ——— Interactive Demo Section ——— */
.demo-section {
    margin-bottom: 100px;
    display: flex;
    gap: 60px;
    align-items: center;
}
.demo-content { flex: 1; }
.demo-visual {
    flex: 1;
    position: relative;
    height: 400px;
}
.demo-content h2 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: #f1f5f9;
    letter-spacing: -1px;
    margin-bottom: 18px;
}
.demo-content p {
    font-size: 1.05rem;
    color: #94a3b8;
    line-height: 1.7;
    margin-bottom: 28px;
}
.demo-features {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 14px;
}
.demo-features li {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 0.95rem;
    color: #cbd5e1;
    padding: 10px 16px;
    background: rgba(17,24,39,0.4);
    border: 1px solid rgba(255,255,255,0.04);
    border-radius: 12px;
    transition: all 0.3s ease;
}
.demo-features li:hover {
    border-color: rgba(99,102,241,0.3);
    background: rgba(99,102,241,0.06);
    transform: translateX(6px);
}
.demo-features li .check-icon {
    width: 24px; height: 24px;
    background: rgba(34,197,94,0.15);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #22c55e;
    font-size: 0.75rem;
    flex-shrink: 0;
}

/* ——— Mock Dashboard Preview ——— */
.mock-dashboard {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: rgba(17, 24, 39, 0.7);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
    animation: float-preview 6s ease-in-out infinite;
}
@keyframes float-preview {
    0%, 100% { transform: translateY(0) rotate(1deg); }
    50% { transform: translateY(-12px) rotate(-1deg); }
}
.mock-titlebar {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 14px 18px;
    background: rgba(0,0,0,0.3);
    border-bottom: 1px solid rgba(255,255,255,0.06);
}
.mock-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
}
.mock-content {
    padding: 20px;
}
.mock-score-circle {
    width: 100px; height: 100px;
    border-radius: 50%;
    border: 4px solid rgba(99,102,241,0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 10px auto 16px;
    position: relative;
}
.mock-score-circle::after {
    content: '';
    position: absolute;
    width: 100%; height: 100%;
    border-radius: 50%;
    border: 4px solid transparent;
    border-top-color: #6366f1;
    border-right-color: #818cf8;
    animation: spin-slow 3s linear infinite;
}
.mock-score-val {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #818cf8;
}
.mock-bars {
    display: flex; flex-direction: column; gap: 10px;
    margin-top: 16px;
}
.mock-bar-label {
    font-size: 0.72rem;
    color: #64748b;
    margin-bottom: 3px;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
}
.mock-bar-track {
    height: 6px;
    background: rgba(255,255,255,0.06);
    border-radius: 10px;
    overflow: hidden;
}
.mock-bar-fill {
    height: 100%;
    border-radius: 10px;
    animation: bar-grow 2s ease forwards;
}
@keyframes bar-grow {
    0% { width: 0%; }
}

/* ——— Final CTA Section ——— */
.final-cta {
    text-align: center;
    padding: 80px 20px;
    position: relative;
    margin-bottom: 40px;
}
.final-cta h2 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 3rem;
    font-weight: 700;
    color: #f1f5f9;
    letter-spacing: -1.5px;
    margin-bottom: 16px;
}
.final-cta p {
    font-size: 1.1rem;
    color: #94a3b8;
    margin-bottom: 36px;
}
.final-cta-glow {
    position: absolute;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(99,102,241,0.15), transparent);
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    border-radius: 50%;
    filter: blur(60px);
    pointer-events: none;
}

/* ——— Footer ——— */
.page-footer {
    text-align: center;
    padding: 40px 0;
    border-top: 1px solid rgba(255,255,255,0.04);
    color: #475569;
    font-size: 0.82rem;
}
.page-footer a {
    color: #6366f1;
    text-decoration: none;
}

/* ——— Scroll Reveal ——— */
.reveal {
    opacity: 0;
    transform: translateY(40px);
    transition: all 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}
.reveal.visible {
    opacity: 1;
    transform: translateY(0);
}

/* ——— Mobile ——— */
@media (max-width: 768px) {
    .features-grid { grid-template-columns: 1fr; }
    .hero-title { font-size: 2.5rem; }
    .demo-section { flex-direction: column; }
    .steps-row { flex-direction: column; gap: 30px; }
    .steps-row::before { display: none; }
    .stats-bar { flex-direction: column; gap: 30px; }
    .nav-center { display: none; }
    .testimonials-track { animation-duration: 15s; }
}
</style>
</head>
<body>

<!-- Loading Screen -->
<div class="loading-screen" id="loadingScreen">
    <div class="loading-logo">CF</div>
    <div class="loading-bar-track">
        <div class="loading-bar-fill"></div>
    </div>
    <div class="loading-text">Forging your experience</div>
</div>

<!-- Custom Cursor -->
<div class="cursor-dot" id="cursorDot"></div>
<div class="cursor-ring" id="cursorRing"></div>
<div class="cursor-glow" id="cursorGlow"></div>

<!-- Background -->
<div class="bg-canvas">
    <div class="bg-orb"></div>
    <div class="bg-orb"></div>
    <div class="bg-orb"></div>
    <div class="bg-orb"></div>
</div>
<div class="grid-overlay"></div>

<!-- Main Content -->
<div class="main-content">

    <!-- TOP BAR -->
    <div class="top-bar">
        <a class="brand-link" onclick="navigateTo('landing')">
            <div class="brand-logo">CF</div>
            <div class="brand-name">CareerForge</div>
        </a>
        <div class="nav-center">
            <a class="nav-link" href="#features">Features</a>
            <a class="nav-link" href="#how-it-works">How It Works</a>
            <a class="nav-link" href="#demo">Live Demo</a>
            <a class="nav-link" href="#testimonials">Testimonials</a>
        </div>
        <div class="auth-btns">
            <button class="btn-signin" onclick="navigateTo('signin')">Sign In</button>
            <button class="btn-signup" onclick="navigateTo('signup')">Sign Up</button>
        </div>
    </div>

    <!-- HERO -->
    <div class="hero-section">
        <div class="hero-badge">
            <span class="pulse-dot"></span>
            Trusted by 500+ students
        </div>
        <h1 class="hero-title">
            <span class="line1">Forge Your</span>
            <span class="line2">Career Path</span>
            <span class="line3">with AI</span>
        </h1>
        <p class="hero-subtitle">
            AI-powered career coaching that adapts to you. Master interviews, build killer resumes,
            crush DSA, and land your dream job — all in one platform.
        </p>
        <div class="hero-ctas">
            <button class="cta-primary" onclick="navigateTo('signup')">
                🚀 Get Started Free
            </button>
            <button class="cta-secondary" onclick="navigateTo('signin')">
                Sign In →
            </button>
        </div>

        <!-- Real-Time Collaborative Animation -->
        <div class="collab-avatars">
            <div class="collab-avatar">AK</div>
            <div class="collab-avatar">PR</div>
            <div class="collab-avatar">SM</div>
            <div class="collab-avatar">VK</div>
            <div class="collab-avatar">+5</div>
            <span class="collab-text">
                <strong>12 students</strong> active now
                <span class="typing-indicator">
                    <span></span><span></span><span></span>
                </span>
            </span>
        </div>
    </div>

    <!-- FEATURES -->
    <div id="features" class="reveal">
        <div class="section-title-area">
            <div class="section-tag">Features</div>
            <h2 class="section-title">Everything You Need</h2>
            <p class="section-desc">Powerful AI-driven tools built for students and job seekers who want results.</p>
        </div>
        <div class="features-grid">
            <div class="feature-card" style="--glow-color: rgba(99,102,241,0.4); --glow-color-dim: rgba(99,102,241,0.08);">
                <div class="feature-icon" style="background: rgba(99,102,241,0.12);">🏠</div>
                <h3>Smart Dashboard</h3>
                <p>Track placement readiness, DSA progress, aptitude score, and daily streak — all at a glance.</p>
                <div class="feature-arrow">→</div>
            </div>
            <div class="feature-card" style="--glow-color: rgba(34,197,94,0.4); --glow-color-dim: rgba(34,197,94,0.08);">
                <div class="feature-icon" style="background: rgba(34,197,94,0.12);">📄</div>
                <h3>Resume Analyzer</h3>
                <p>Upload your resume, get instant AI feedback — strengths, weaknesses, missing skills, and tips.</p>
                <div class="feature-arrow">→</div>
            </div>
            <div class="feature-card" style="--glow-color: rgba(245,158,11,0.4); --glow-color-dim: rgba(245,158,11,0.08);">
                <div class="feature-icon" style="background: rgba(245,158,11,0.12);">📊</div>
                <h3>Placement Predictor</h3>
                <p>AI predicts your placement probability and gives actionable steps to boost your score.</p>
                <div class="feature-arrow">→</div>
            </div>
            <div class="feature-card" style="--glow-color: rgba(167,139,250,0.4); --glow-color-dim: rgba(167,139,250,0.08);">
                <div class="feature-icon" style="background: rgba(167,139,250,0.12);">🧠</div>
                <h3>Adaptive Learning</h3>
                <p>Personalized 7-day sprints targeting your weak areas with curated tasks and problems.</p>
                <div class="feature-arrow">→</div>
            </div>
            <div class="feature-card" style="--glow-color: rgba(56,189,248,0.4); --glow-color-dim: rgba(56,189,248,0.08);">
                <div class="feature-icon" style="background: rgba(56,189,248,0.12);">🤖</div>
                <h3>AI Mentor Chat</h3>
                <p>Chat with your AI career coach for advice on interviews, DSA strategies, and more.</p>
                <div class="feature-arrow">→</div>
            </div>
            <div class="feature-card" style="--glow-color: rgba(244,63,94,0.4); --glow-color-dim: rgba(244,63,94,0.08);">
                <div class="feature-icon" style="background: rgba(244,63,94,0.12);">🎤</div>
                <h3>Mock Interviews</h3>
                <p>Practice with AI-generated technical questions, scored on correctness, clarity, and depth.</p>
                <div class="feature-arrow">→</div>
            </div>
        </div>
    </div>

    <!-- HOW IT WORKS -->
    <div id="how-it-works" class="steps-section reveal">
        <div class="section-title-area">
            <div class="section-tag">How It Works</div>
            <h2 class="section-title">3 Simple Steps</h2>
            <p class="section-desc">From zero to placement-ready in record time.</p>
        </div>
        <div class="steps-row">
            <div class="step-item">
                <div class="step-num" style="background: linear-gradient(135deg, #6366f1, #818cf8); box-shadow: 0 6px 24px rgba(99,102,241,0.3);">1</div>
                <h3>Create Your Profile</h3>
                <p>Sign up and tell us your career goal — SDE, Data Science, Product, or more.</p>
            </div>
            <div class="step-item">
                <div class="step-num" style="background: linear-gradient(135deg, #22c55e, #4ade80); box-shadow: 0 6px 24px rgba(34,197,94,0.3);">2</div>
                <h3>Get AI Insights</h3>
                <p>Our AI analyzes your skills, resume, and progress to create a personalized plan.</p>
            </div>
            <div class="step-item">
                <div class="step-num" style="background: linear-gradient(135deg, #f59e0b, #fbbf24); box-shadow: 0 6px 24px rgba(245,158,11,0.3);">3</div>
                <h3>Land Your Dream Job</h3>
                <p>Follow your adaptive learning path, practice interviews, watch your score climb.</p>
            </div>
        </div>
    </div>

    <!-- INTERACTIVE DEMO -->
    <div id="demo" class="demo-section reveal">
        <div class="demo-content">
            <div class="section-tag">Live Preview</div>
            <h2>See It In Action</h2>
            <p>Your personalized dashboard gives you real-time insights into every aspect of your career preparation journey.</p>
            <ul class="demo-features">
                <li>
                    <span class="check-icon">✓</span>
                    Real-time placement score tracking
                </li>
                <li>
                    <span class="check-icon">✓</span>
                    AI-generated personalized study plans
                </li>
                <li>
                    <span class="check-icon">✓</span>
                    Mock interview with instant feedback
                </li>
                <li>
                    <span class="check-icon">✓</span>
                    Resume analysis against industry standards
                </li>
                <li>
                    <span class="check-icon">✓</span>
                    Progress tracking with visual analytics
                </li>
            </ul>
        </div>
        <div class="demo-visual">
            <div class="mock-dashboard">
                <div class="mock-titlebar">
                    <div class="mock-dot" style="background:#ef4444;"></div>
                    <div class="mock-dot" style="background:#f59e0b;"></div>
                    <div class="mock-dot" style="background:#22c55e;"></div>
                    <span style="margin-left: 12px; font-size: 0.75rem; color: #64748b;">CareerForge Dashboard</span>
                </div>
                <div class="mock-content">
                    <div style="text-align:center; font-size:0.75rem; color:#64748b; text-transform:uppercase; letter-spacing:1.5px; font-weight:600;">Placement Score</div>
                    <div class="mock-score-circle">
                        <span class="mock-score-val" id="mockScore">0</span>
                    </div>
                    <div class="mock-bars">
                        <div>
                            <div class="mock-bar-label">DSA Progress</div>
                            <div class="mock-bar-track"><div class="mock-bar-fill" style="width:72%; background:linear-gradient(90deg, #6366f1, #818cf8);"></div></div>
                        </div>
                        <div>
                            <div class="mock-bar-label">Aptitude</div>
                            <div class="mock-bar-track"><div class="mock-bar-fill" style="width:85%; background:linear-gradient(90deg, #22c55e, #4ade80);"></div></div>
                        </div>
                        <div>
                            <div class="mock-bar-label">Interview Ready</div>
                            <div class="mock-bar-track"><div class="mock-bar-fill" style="width:58%; background:linear-gradient(90deg, #f59e0b, #fbbf24);"></div></div>
                        </div>
                        <div>
                            <div class="mock-bar-label">Resume Score</div>
                            <div class="mock-bar-track"><div class="mock-bar-fill" style="width:65%; background:linear-gradient(90deg, #f43f5e, #fb7185);"></div></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- STATS BAR -->
    <div class="stats-bar reveal">
        <div class="stat-item">
            <div class="stat-num counter" data-target="500" style="--stat-color-1:#6366f1;--stat-color-2:#818cf8;">0+</div>
            <div class="stat-label">Active Students</div>
        </div>
        <div class="stat-item">
            <div class="stat-num counter" data-target="1200" style="--stat-color-1:#22c55e;--stat-color-2:#4ade80;">0+</div>
            <div class="stat-label">Mock Interviews</div>
        </div>
        <div class="stat-item">
            <div class="stat-num counter" data-target="85" style="--stat-color-1:#f59e0b;--stat-color-2:#fbbf24;">0%</div>
            <div class="stat-label">Placement Rate</div>
        </div>
        <div class="stat-item">
            <div class="stat-num" style="--stat-color-1:#a78bfa;--stat-color-2:#c4b5fd;">100%</div>
            <div class="stat-label">Free Forever</div>
        </div>
    </div>

    <!-- TESTIMONIALS -->
    <div id="testimonials" class="testimonials-section reveal">
        <div class="section-title-area">
            <div class="section-tag">Testimonials</div>
            <h2 class="section-title">Loved by Students</h2>
            <p class="section-desc">See what our users have to say about their CareerForge experience.</p>
        </div>
        <div style="overflow:hidden;">
            <div class="testimonials-track">
                <div class="testimonial-card">
                    <div class="testimonial-stars">★★★★★</div>
                    <div class="testimonial-text">"CareerForge helped me crack my Google interview. The adaptive learning path targeted exactly what I needed."</div>
                    <div class="testimonial-author">
                        <div class="testimonial-avatar" style="background:linear-gradient(135deg,#6366f1,#818cf8);">AK</div>
                        <div>
                            <div class="testimonial-name">Arjun Kumar</div>
                            <div class="testimonial-role">SDE @ Google</div>
                        </div>
                    </div>
                </div>
                <div class="testimonial-card">
                    <div class="testimonial-stars">★★★★★</div>
                    <div class="testimonial-text">"The mock interview feature is incredible. Real-time feedback on my answers boosted my confidence 10x."</div>
                    <div class="testimonial-author">
                        <div class="testimonial-avatar" style="background:linear-gradient(135deg,#22c55e,#4ade80);">PR</div>
                        <div>
                            <div class="testimonial-name">Priya Reddy</div>
                            <div class="testimonial-role">SDE @ Microsoft</div>
                        </div>
                    </div>
                </div>
                <div class="testimonial-card">
                    <div class="testimonial-stars">★★★★★</div>
                    <div class="testimonial-text">"From 45% to 88% placement score in 3 weeks. The AI mentor chat is like having a personal career coach 24/7."</div>
                    <div class="testimonial-author">
                        <div class="testimonial-avatar" style="background:linear-gradient(135deg,#f59e0b,#fbbf24);">SM</div>
                        <div>
                            <div class="testimonial-name">Sneha Mehta</div>
                            <div class="testimonial-role">Data Analyst @ Amazon</div>
                        </div>
                    </div>
                </div>
                <div class="testimonial-card">
                    <div class="testimonial-stars">★★★★★</div>
                    <div class="testimonial-text">"Best career prep tool I've used. The resume analyzer found gaps I never noticed and helped me fix them fast."</div>
                    <div class="testimonial-author">
                        <div class="testimonial-avatar" style="background:linear-gradient(135deg,#f43f5e,#fb7185);">VK</div>
                        <div>
                            <div class="testimonial-name">Vikram Krishna</div>
                            <div class="testimonial-role">SDE @ Flipkart</div>
                        </div>
                    </div>
                </div>
                <div class="testimonial-card">
                    <div class="testimonial-stars">★★★★★</div>
                    <div class="testimonial-text">"The consistency tracking and daily streaks kept me motivated throughout my placement prep season."</div>
                    <div class="testimonial-author">
                        <div class="testimonial-avatar" style="background:linear-gradient(135deg,#06b6d4,#22d3ee);">NP</div>
                        <div>
                            <div class="testimonial-name">Nisha Patel</div>
                            <div class="testimonial-role">SDE @ Razorpay</div>
                        </div>
                    </div>
                </div>
                <!-- Duplicate for seamless loop -->
                <div class="testimonial-card">
                    <div class="testimonial-stars">★★★★★</div>
                    <div class="testimonial-text">"CareerForge helped me crack my Google interview. The adaptive learning path targeted exactly what I needed."</div>
                    <div class="testimonial-author">
                        <div class="testimonial-avatar" style="background:linear-gradient(135deg,#6366f1,#818cf8);">AK</div>
                        <div>
                            <div class="testimonial-name">Arjun Kumar</div>
                            <div class="testimonial-role">SDE @ Google</div>
                        </div>
                    </div>
                </div>
                <div class="testimonial-card">
                    <div class="testimonial-stars">★★★★★</div>
                    <div class="testimonial-text">"The mock interview feature is incredible. Real-time feedback on my answers boosted my confidence 10x."</div>
                    <div class="testimonial-author">
                        <div class="testimonial-avatar" style="background:linear-gradient(135deg,#22c55e,#4ade80);">PR</div>
                        <div>
                            <div class="testimonial-name">Priya Reddy</div>
                            <div class="testimonial-role">SDE @ Microsoft</div>
                        </div>
                    </div>
                </div>
                <div class="testimonial-card">
                    <div class="testimonial-stars">★★★★★</div>
                    <div class="testimonial-text">"From 45% to 88% placement score in 3 weeks. The AI mentor chat is like having a personal career coach 24/7."</div>
                    <div class="testimonial-author">
                        <div class="testimonial-avatar" style="background:linear-gradient(135deg,#f59e0b,#fbbf24);">SM</div>
                        <div>
                            <div class="testimonial-name">Sneha Mehta</div>
                            <div class="testimonial-role">Data Analyst @ Amazon</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- FINAL CTA -->
    <div class="final-cta reveal">
        <div class="final-cta-glow"></div>
        <h2>Ready to Forge Your Future?</h2>
        <p>Join hundreds of students already using CareerForge to land their dream jobs.</p>
        <button class="cta-primary" style="font-size: 1.1rem; padding: 18px 44px;" onclick="navigateTo('signup')">
            🔥 Start Your Journey Now
        </button>
    </div>

    <!-- FOOTER -->
    <div class="page-footer">
        Built with ❤️ by Team Renegades  •  Hack AI 2.0
    </div>
</div>

<script>
// ——— Loading Screen ———
setTimeout(() => {
    document.getElementById('loadingScreen').classList.add('hidden');
}, 2200);

// ——— Custom Cursor ———
const dot = document.getElementById('cursorDot');
const ring = document.getElementById('cursorRing');
const cursorGlow = document.getElementById('cursorGlow');
const bgOrbs = document.querySelectorAll('.bg-orb');
const gridOverlay = document.querySelector('.grid-overlay');
let mouseX = 0, mouseY = 0;
let ringX = 0, ringY = 0;
let glowX = 0, glowY = 0;
let lastSparkleTime = 0;

document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
    dot.style.left = mouseX - 5 + 'px';
    dot.style.top = mouseY - 5 + 'px';

    // Star sparkle trail removed per request
    // const now = performance.now();
    // if (now - lastSparkleTime > 40) {
    //     createSparkle(mouseX, mouseY);
    //     lastSparkleTime = now;
    // }

    // ——— Background Glow follows cursor ———
    cursorGlow.style.left = mouseX + 'px';
    cursorGlow.style.top = mouseY + 'px';

    // ——— Background Orbs bend toward cursor ———
    const cx = (mouseX / window.innerWidth - 0.5) * 2;
    const cy = (mouseY / window.innerHeight - 0.5) * 2;
    bgOrbs.forEach((orb, i) => {
        const intensity = [40, 30, 25, 20][i] || 20;
        const offsetX = cx * intensity;
        const offsetY = cy * intensity;
        orb.style.transform = `translate(${offsetX}px, ${offsetY}px)`;
    });

    // ——— Grid lines bend near cursor ———
    const gridShiftX = cx * 8;
    const gridShiftY = cy * 8;
    gridOverlay.style.backgroundPosition = `${gridShiftX}px ${gridShiftY}px`;
});

// ——— Ring follows cursor at high FPS with faster lerp ———
function animateRing() {
    ringX += (mouseX - ringX) * 0.35;
    ringY += (mouseY - ringY) * 0.35;
    ring.style.left = ringX - 20 + 'px';
    ring.style.top = ringY - 20 + 'px';

    // Smooth glow follow
    glowX += (mouseX - glowX) * 0.08;
    glowY += (mouseY - glowY) * 0.08;

    requestAnimationFrame(animateRing);
}
animateRing();

// Cursor hover effects
document.querySelectorAll('button, a, .feature-card, .nav-link, .testimonial-card').forEach(el => {
    el.addEventListener('mouseenter', () => {
        dot.style.transform = 'scale(2.5)';
        dot.style.background = 'radial-gradient(circle, #fff 0%, #a78bfa 60%, transparent 100%)';
        ring.style.width = '56px';
        ring.style.height = '56px';
        ring.style.borderColor = 'rgba(167,139,250,0.7)';
        ring.style.boxShadow = '0 0 20px rgba(167,139,250,0.3)';
    });
    el.addEventListener('mouseleave', () => {
        dot.style.transform = 'scale(1)';
        dot.style.background = 'radial-gradient(circle, #fff 0%, #818cf8 60%, transparent 100%)';
        ring.style.width = '40px';
        ring.style.height = '40px';
        ring.style.borderColor = 'rgba(129,140,248,0.5)';
        ring.style.boxShadow = '0 0 12px rgba(129,140,248,0.15)';
    });
});

// ——— Star Sparkle Particles ———
function createSparkle(x, y) {
    const sparkle = document.createElement('div');
    sparkle.className = 'sparkle';
    const size = Math.random() * 8 + 4;
    const colors = ['#818cf8', '#a78bfa', '#6366f1', '#06b6d4', '#f43f5e', '#c084fc', '#fbbf24', '#fff'];
    const color = colors[Math.floor(Math.random() * colors.length)];
    const tx = (Math.random() - 0.5) * 120;
    const ty = (Math.random() - 0.5) * 120;
    const rotation = Math.random() * 360;

    sparkle.style.cssText = `
        left: ${x}px; top: ${y}px;
        width: ${size}px; height: ${size}px;
        background: ${color};
        box-shadow: 0 0 ${size * 3}px ${color}, 0 0 ${size}px #fff;
        --tx: ${tx}px; --ty: ${ty}px;
        transform: rotate(${rotation}deg);
    `;
    document.body.appendChild(sparkle);
    setTimeout(() => sparkle.remove(), 1000);
}

// ——— Feature Card Mouse Follow Glow ———
document.querySelectorAll('.feature-card').forEach(card => {
    card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = ((e.clientX - rect.left) / rect.width) * 100;
        const y = ((e.clientY - rect.top) / rect.height) * 100;
        card.style.setProperty('--mouse-x', x + '%');
        card.style.setProperty('--mouse-y', y + '%');
    });
});

// ——— Scroll Reveal ———
function revealOnScroll() {
    document.querySelectorAll('.reveal').forEach(el => {
        const rect = el.getBoundingClientRect();
        if (rect.top < window.innerHeight - 80) {
            el.classList.add('visible');
        }
    });
}
window.addEventListener('scroll', revealOnScroll);
setTimeout(revealOnScroll, 100);

// ——— Counter Animation ———
let countersAnimated = false;
function animateCounters() {
    if (countersAnimated) return;
    const counters = document.querySelectorAll('.counter');
    counters.forEach(counter => {
        const rect = counter.getBoundingClientRect();
        if (rect.top < window.innerHeight) {
            countersAnimated = true;
            const target = parseInt(counter.dataset.target);
            const suffix = counter.textContent.includes('%') ? '%' : '+';
            let current = 0;
            const step = Math.ceil(target / 60);
            const interval = setInterval(() => {
                current += step;
                if (current >= target) {
                    current = target;
                    clearInterval(interval);
                }
                counter.textContent = current.toLocaleString() + suffix;
            }, 25);
        }
    });
}
window.addEventListener('scroll', animateCounters);
setTimeout(animateCounters, 2500);

// ——— Mock Dashboard Score Counter ———
setTimeout(() => {
    const scoreEl = document.getElementById('mockScore');
    let val = 0;
    const interval = setInterval(() => {
        val += 1;
        if (val >= 78) { val = 78; clearInterval(interval); }
        scoreEl.textContent = val + '%';
    }, 35);
}, 2500);

// ——— Smooth scroll for nav links ———
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = link.getAttribute('href').substring(1);
        const targetEl = document.getElementById(targetId);
        if (targetEl) {
            targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});
// ——— Navigation helper (direct parent URL change) ———
function navigateTo(page) {
    try {
        // Try direct parent location change (works if same-origin)
        window.parent.location.href = window.parent.location.pathname + '?page=' + page;
    } catch(e) {
        // Fallback: try top-level navigation
        try {
            window.top.location.href = '/?page=' + page;
        } catch(e2) {
            // Last resort: postMessage
            window.parent.postMessage({type: 'streamlit_navigate', page: page}, '*');
        }
    }
}
</script>
</body>
</html>
    """
    
    # Write the HTML file
    landing_path = os.path.join(static_dir, "landing.html")
    with open(landing_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    # Embed via raw iframe without sandbox restrictions
    st.markdown(
        '<iframe src="/app/static/landing.html" '
        'width="100%" height="4000" frameborder="0" '
        'style="border:none; display:block;" '
        'allow="scripts"></iframe>',
        unsafe_allow_html=True
    )


# -----------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------
def main():
    load_css()
    init_state()

    # Initialize page routing
    if "show_page" not in st.session_state:
        st.session_state.show_page = "landing"

    # Read navigation from URL query params (set by JS listener)
    qp = st.query_params
    if "page" in qp:
        requested = qp["page"]
        if requested in ("signin", "signup", "landing"):
            st.session_state.show_page = requested
            st.query_params.clear()
            st.rerun()

    # If authenticated, force to dashboard
    if st.session_state.authenticated:
        st.session_state.show_page = "dashboard"

    # Route to the correct page
    page = st.session_state.show_page

    if page == "landing":
        render_landing_page()

    elif page == "signin":
        render_signin_page()
    elif page == "signup":
        render_signup_page()
    elif page == "dashboard":
        if not st.session_state.authenticated:
            st.session_state.show_page = "landing"
            st.rerun()
            return

        render_authenticated_navbar()

        # Tab navigation
        tabs = st.tabs(
            [
                "🏠 Dashboard",
                "📄 Resume",
                "📊 Predictor",
                "🧠 Learning",
                "🤖 Mentor",
                "🎤 Interview",
                "📈 Progress",
            ]
        )

        with tabs[0]:
            render_dashboard()
        with tabs[1]:
            render_resume_analyzer()
        with tabs[2]:
            render_placement_predictor()
        with tabs[3]:
            render_adaptive_learning()
        with tabs[4]:
            render_ai_mentor()
        with tabs[5]:
            render_mock_interview()
        with tabs[6]:
            render_progress_tracking()


if __name__ == "__main__":
    main()
