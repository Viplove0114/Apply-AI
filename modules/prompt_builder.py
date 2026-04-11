"""
prompt_builder.py — Assembles the LLM prompt for generating
cover letters and cold emails.

Handles:
  - Output type (Cover Letter / Cold Email)
  - Output length (Small / Large)
  - Tone selection (Professional, Warm, Confident, Casual, Formal, Creative)
  - Humanized writing instructions
"""


# ── Tone descriptions for the LLM ────────────────────────────
_TONE_DESCRIPTIONS: dict[str, str] = {
    "Professional": (
        "Use a professional, polished tone. Be clear, structured, and business-appropriate. "
        "Demonstrate competence and reliability without being stiff."
    ),
    "Warm": (
        "Use a warm, friendly, and approachable tone. Show genuine enthusiasm and personal touch. "
        "Make the reader feel a human connection while maintaining professionalism."
    ),
    "Confident": (
        "Use a confident, assertive tone. Lead with accomplishments and strong statements. "
        "Project self-assurance without coming across as arrogant."
    ),
    "Casual": (
        "Use a casual, conversational tone. Write as if talking to a peer. "
        "Keep it natural and relaxed while still highlighting your qualifications."
    ),
    "Formal": (
        "Use a formal, highly structured tone. Follow traditional business writing conventions. "
        "Be respectful, precise, and meticulously organized."
    ),
    "Creative": (
        "Use a creative, unique tone. Stand out with an original opening or storytelling. "
        "Take a memorable, slightly unconventional approach while staying relevant."
    ),
}


def build_prompt(
    resume: str,
    job_description: str,
    output_type: str,
    output_length: int,
    tone: str,
) -> str:
    """
    Build the full prompt to send to the LLM.

    Args:
        resume:          The user's resume text.
        job_description: The job description or post text.
        output_type:     "Cover Letter" or "Cold Email".
        output_length:   Target word count (e.g. 250 or 500).
        tone:            One of the TONE_OPTIONS from config.

    Returns:
        A fully assembled prompt string.
    """
    tone_instruction = _TONE_DESCRIPTIONS.get(tone, _TONE_DESCRIPTIONS["Professional"])

    prompt = f"""
You are tasked with writing a {output_type.lower()} for a job applicant.

══════════════════════════════════════════
INSTRUCTIONS
══════════════════════════════════════════

1. **Output type**: Write a {output_type.lower()}.
2. **Word count**: Aim for approximately {output_length} words. Do not exceed this limit significantly.
3. **Tone**: {tone_instruction}
4. **Writing style — CRITICAL**:
   - Write in a HUMANIZED way. This must read like a real person wrote it, NOT an AI.
   - Use natural sentence variation — mix short and long sentences.
   - Avoid buzzwords like "synergy", "leverage", "cutting-edge", "dynamic", "passionate" — use real, specific language.
   - Do NOT start with generic openers like "I am writing to express my interest in..."
   - Include one or two subtle imperfections that a human might write — a slightly informal phrase, a personal aside, or a conversational transition.
   - Show genuine personality and specific details from the resume.
5. **Content**:
   - Map the candidate's skills and experience to the job requirements.
   - Highlight 2-3 most relevant achievements or experiences from the resume.
   - If writing a cold email: include a clear, specific call-to-action and a compelling subject line at the top.
   - If writing a cover letter: follow a natural letter structure (greeting → hook → body → closing).
6. **Formatting**:
   - Do NOT include any labels like "Subject:", "Cover Letter:", etc. unless it's a cold email subject line.
   - For cold emails: start with "Subject: ..." on the first line, then leave a blank line before the email body.
   - Do NOT add any explanatory notes, disclaimers, or meta-commentary — ONLY output the {output_type.lower()} itself.

══════════════════════════════════════════
JOB DESCRIPTION
══════════════════════════════════════════

{job_description}

══════════════════════════════════════════
CANDIDATE'S RESUME
══════════════════════════════════════════

{resume}

══════════════════════════════════════════

Now write the {output_type.lower()}. Remember: humanized, {tone.lower()} tone, ~{output_length} words. Output ONLY the final text.
"""
    return prompt.strip()
