"""
config.py — Central configuration for Apply-AI.
All constants, settings, and environment variables live here.
"""

import os
from dotenv import load_dotenv

# ── Load .env ────────────────────────────────────────────────
load_dotenv()

# ── API Keys ─────────────────────────────────────────────────
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")

# ── App Meta ─────────────────────────────────────────────────
APP_TITLE: str = "Apply-AI ✍️"
APP_SUBTITLE: str = "Generate tailored cover letters & cold emails in seconds"
APP_VERSION: str = "1.0.0"

# ── Model Settings ───────────────────────────────────────────
MODEL_NAME: str = "openai/gpt-oss-120b"
MODEL_TEMPERATURE: float = 0.7
MODEL_MAX_TOKENS: int = 2048

# ── Output Length Map (in words) ─────────────────────────────
OUTPUT_LENGTHS: dict[str, int] = {
    "Small (250 words)": 250,
    "Large (500 words)": 500,
}

# ── Output Types ─────────────────────────────────────────────
OUTPUT_TYPES: list[str] = [
    "Cover Letter",
    "Cold Email",
]

# ── Tone Options ─────────────────────────────────────────────
TONE_OPTIONS: list[str] = [
    "Professional",
    "Warm",
    "Confident",
    "Casual",
    "Formal",
    "Creative",
]
