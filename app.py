"""
app.py — Streamlit UI entry point for Apply-AI.

A beautiful, modern interface for generating tailored cover letters
and cold emails using Groq's LLM.
"""

import streamlit as st
from config import (
    APP_TITLE,
    APP_SUBTITLE,
    APP_VERSION,
    OUTPUT_LENGTHS,
    OUTPUT_TYPES,
    TONE_OPTIONS,
    GROQ_API_KEY,
)
from modules.groq_client import generate_response
from modules.resume_parser import parse_pdf, parse_text
from modules.job_fetcher import fetch_from_url
from modules.prompt_builder import build_prompt
from utils.helpers import format_output, count_words


# ══════════════════════════════════════════════════════════════
# Page Configuration
# ══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Apply-AI — Cover Letters & Cold Emails",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ══════════════════════════════════════════════════════════════
# Custom CSS — Modern dark glassmorphism theme
# ══════════════════════════════════════════════════════════════

st.markdown("""
<style>
    /* ── Import Google Font ───────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Global ───────────────────────────────────────────── */
    * {
        font-family: 'Inter', sans-serif !important;
    }

    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 40%, #24243e 100%);
    }

    /* ── Sidebar ──────────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #16153a 0%, #1c1b4b 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }

    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown label,
    section[data-testid="stSidebar"] label {
        color: #c4c4e0 !important;
    }

    /* ── Header ───────────────────────────────────────────── */
    .main-header {
        text-align: center;
        padding: 2rem 0 1rem;
    }

    .main-header h1 {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.3rem;
    }

    .main-header .subtitle {
        font-size: 1.1rem;
        color: #9898c8;
        font-weight: 300;
        letter-spacing: 0.5px;
    }

    .main-header .version-badge {
        display: inline-block;
        margin-top: 0.5rem;
        padding: 0.2rem 0.8rem;
        background: rgba(102, 126, 234, 0.15);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 20px;
        font-size: 0.75rem;
        color: #667eea;
        letter-spacing: 1px;
        font-weight: 500;
    }

    /* ── Cards / Glass panels ─────────────────────────────── */
    .glass-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
    }

    .glass-card h3 {
        color: #e0e0ff;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* ── Output card ──────────────────────────────────────── */
    .output-card {
        background: rgba(102, 126, 234, 0.06);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 16px;
        padding: 2rem;
        margin-top: 1rem;
        line-height: 1.8;
        color: #d4d4f0;
        font-size: 0.95rem;
        white-space: pre-wrap;
    }

    /* ── Streamlit overrides ──────────────────────────────── */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #e0e0ff !important;
        font-size: 0.9rem !important;
    }

    .stTextArea textarea:focus {
        border-color: rgba(102, 126, 234, 0.5) !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.15) !important;
    }

    .stTextInput input {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #e0e0ff !important;
    }

    .stTextInput input:focus {
        border-color: rgba(102, 126, 234, 0.5) !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.15) !important;
    }

    div.stRadio > label {
        color: #c4c4e0 !important;
    }

    /* ── Generate button ──────────────────────────────────── */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.45) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* ── Selectbox & Radio ────────────────────────────────── */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #e0e0ff !important;
    }

    /* ── File uploader ────────────────────────────────────── */
    .stFileUploader > div {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px dashed rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
    }

    /* ── Stats row ────────────────────────────────────────── */
    .stats-row {
        display: flex;
        gap: 1rem;
        margin-top: 0.8rem;
        margin-bottom: 0.5rem;
    }

    .stat-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.3rem 0.8rem;
        background: rgba(102, 126, 234, 0.12);
        border: 1px solid rgba(102, 126, 234, 0.25);
        border-radius: 20px;
        font-size: 0.8rem;
        color: #a0b0ff;
        font-weight: 500;
    }

    /* ── Warning / info boxes ─────────────────────────────── */
    .stAlert {
        background: rgba(255, 255, 255, 0.03) !important;
        border-radius: 12px !important;
    }

    /* ── Divider ──────────────────────────────────────────── */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.3), transparent);
        margin: 1.5rem 0;
    }

    /* ── Sidebar Tone Pills ───────────────────────────────── */
    .sidebar-section-title {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #667eea !important;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }

    /* ── Footer ───────────────────────────────────────────── */
    .app-footer {
        text-align: center;
        padding: 2rem 0 1rem;
        color: #5a5a8a;
        font-size: 0.8rem;
    }

    .app-footer a {
        color: #667eea;
        text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# Header
# ══════════════════════════════════════════════════════════════

st.markdown(f"""
<div class="main-header">
    <h1>{APP_TITLE}</h1>
    <div class="subtitle">{APP_SUBTITLE}</div>
    <div class="version-badge">v{APP_VERSION}</div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# Sidebar — Settings
# ══════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Output Type
    st.markdown('<p class="sidebar-section-title">📝 Output Type</p>', unsafe_allow_html=True)
    output_type = st.selectbox(
        "Output Type",
        OUTPUT_TYPES,
        label_visibility="collapsed",
        help="Choose between a Cover Letter or a Cold Email",
    )

    # Tone
    st.markdown('<p class="sidebar-section-title">🎭 Tone</p>', unsafe_allow_html=True)
    tone = st.selectbox(
        "Tone",
        TONE_OPTIONS,
        label_visibility="collapsed",
        help="Set the overall tone of your generated text",
    )

    # Output Length
    st.markdown('<p class="sidebar-section-title">📏 Output Length</p>', unsafe_allow_html=True)
    output_length_label = st.selectbox(
        "Output Length",
        list(OUTPUT_LENGTHS.keys()),
        label_visibility="collapsed",
        help="Small ≈ 250 words, Large ≈ 500 words",
    )
    output_length = OUTPUT_LENGTHS[output_length_label]

    # API Key Status
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    if GROQ_API_KEY:
        st.success("🔑 Groq API key loaded", icon="✅")
    else:
        st.error("🔑 Groq API key missing — add it to `.env`", icon="❌")

    st.markdown(
        '<div class="section-divider"></div>'
        f'<p style="text-align:center; color:#5a5a8a; font-size:0.75rem;">'
        f'Apply-AI v{APP_VERSION} · Powered by Groq</p>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════
# Main Content — Two input columns
# ══════════════════════════════════════════════════════════════

col_jd, col_resume = st.columns(2, gap="large")


# ── Left Column: Job Description ─────────────────────────────

with col_jd:
    st.markdown("""
    <div class="glass-card">
        <h3>💼 Job Description</h3>
    </div>
    """, unsafe_allow_html=True)

    jd_input_method = st.radio(
        "How would you like to provide the job description?",
        ["📋 Paste Text", "🔗 LinkedIn / URL"],
        horizontal=True,
        key="jd_method",
    )

    if jd_input_method == "📋 Paste Text":
        jd_text = st.text_area(
            "Paste the job description here",
            height=280,
            placeholder="Paste the full job description, requirements, or HR post here...",
            key="jd_text_input",
        )
    else:
        jd_url = st.text_input(
            "Enter the LinkedIn post or job listing URL",
            placeholder="https://www.linkedin.com/posts/...",
            key="jd_url_input",
        )


# ── Right Column: Resume / Profile ───────────────────────────

with col_resume:
    st.markdown("""
    <div class="glass-card">
        <h3>📄 Resume / Profile</h3>
    </div>
    """, unsafe_allow_html=True)

    resume_input_method = st.radio(
        "How would you like to provide your resume?",
        ["📋 Paste Text", "📎 Upload PDF"],
        horizontal=True,
        key="resume_method",
    )

    if resume_input_method == "📋 Paste Text":
        resume_text = st.text_area(
            "Paste your resume content here",
            height=280,
            placeholder="Paste your resume, skills, experience, and education here...",
            key="resume_text_input",
        )
    else:
        resume_file = st.file_uploader(
            "Upload your resume (PDF)",
            type=["pdf"],
            key="resume_file_input",
            help="Upload a PDF version of your resume",
        )


# ══════════════════════════════════════════════════════════════
# Generate Button
# ══════════════════════════════════════════════════════════════

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

generate_col = st.columns([1, 2, 1])
with generate_col[1]:
    generate_clicked = st.button(
        f"✨  Generate {output_type}",
        use_container_width=True,
        key="generate_btn",
    )


# ══════════════════════════════════════════════════════════════
# Processing & Output
# ══════════════════════════════════════════════════════════════

if generate_clicked:
    # ── Collect Job Description ───────────────────────────────
    job_description = None
    with st.spinner(""):
        try:
            if jd_input_method == "📋 Paste Text":
                jd_raw = jd_text if "jd_text" in dir() else ""
                if not jd_raw or not jd_raw.strip():
                    st.error("⚠️ Please provide a job description.")
                    st.stop()
                job_description = jd_raw.strip()
            else:
                jd_url_val = jd_url if "jd_url" in dir() else ""
                if not jd_url_val or not jd_url_val.strip():
                    st.error("⚠️ Please provide a URL.")
                    st.stop()
                with st.status("🔍 Fetching job description from URL...", expanded=True) as status:
                    st.write("Connecting to the page...")
                    job_description = fetch_from_url(jd_url_val.strip())
                    st.write(f"✅ Extracted {count_words(job_description)} words")
                    status.update(label="✅ Job description fetched!", state="complete")
        except ValueError as e:
            st.error(f"❌ {e}")
            st.stop()

    # ── Collect Resume ────────────────────────────────────────
    resume = None
    try:
        if resume_input_method == "📋 Paste Text":
            resume_raw = resume_text if "resume_text" in dir() else ""
            resume = parse_text(resume_raw)
        else:
            resume_file_val = resume_file if "resume_file" in dir() else None
            if not resume_file_val:
                st.error("⚠️ Please upload your resume PDF.")
                st.stop()
            with st.status("📄 Parsing your resume...", expanded=False) as status:
                resume = parse_pdf(resume_file_val)
                status.update(label=f"✅ Resume parsed ({count_words(resume)} words)", state="complete")
    except ValueError as e:
        st.error(f"❌ {e}")
        st.stop()

    # ── Build Prompt & Generate ───────────────────────────────
    prompt = build_prompt(
        resume=resume,
        job_description=job_description,
        output_type=output_type,
        output_length=output_length,
        tone=tone,
    )

    with st.status(f"🤖 Generating your {output_type.lower()}...", expanded=True) as status:
        st.write(f"Model: `llama-3.3-70b-versatile` · Tone: **{tone}** · Target: ~{output_length} words")
        try:
            raw_output = generate_response(prompt)
            result = format_output(raw_output)
            status.update(label=f"✅ {output_type} generated!", state="complete")
        except (ValueError, RuntimeError) as e:
            st.error(f"❌ {e}")
            st.stop()

    # ── Display Result ────────────────────────────────────────
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.markdown(f"### ✨ Your {output_type}")

    # Stats pills
    word_count = count_words(result)
    st.markdown(f"""
    <div class="stats-row">
        <span class="stat-pill">📝 {word_count} words</span>
        <span class="stat-pill">🎭 {tone}</span>
        <span class="stat-pill">📏 {output_length_label}</span>
    </div>
    """, unsafe_allow_html=True)

    # Output in a styled card
    st.markdown(f'<div class="output-card">{result}</div>', unsafe_allow_html=True)

    # Copy button
    st.code(result, language=None)
    st.caption("👆 Click the copy icon in the top-right corner of the code block above to copy.")

    # Option to regenerate with a different tone
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.info("💡 **Tip:** Change the **Tone** or **Output Length** in the sidebar and click Generate again for a different version!", icon="💡")


# ══════════════════════════════════════════════════════════════
# Footer
# ══════════════════════════════════════════════════════════════

st.markdown(f"""
<div class="app-footer">
    Built with ❤️ using Streamlit & Groq · 
    <a href="https://console.groq.com/keys" target="_blank">Get your Groq API key</a>
</div>
""", unsafe_allow_html=True)
