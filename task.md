Let's build a project. The goal is to give link of LinkedIn posts(where the hr mentioning the jd or requirements)or paste the job description and my resume(as text or as a file) as input and chat bot will respond a custom email or cover letter in a humanize way possible.


some more instructions:

1. i want this to be a python AI project
2. in resume and profile section i also want an option to upload a resume with
3. add an option to select that the user want a large output, or a small output (mention it in the prompt that if user selects large that means 500 words and small means 250 words).
4. mention in prompt that wirte in a humanize way possible.
5. i want to use Groq api key in this.
6. build a complete modular coding structure.

A rough sketch of the folder structure:

apply-ai/
├── app.py                 ← Streamlit UI entry point
├── config.py              ← All constants & settings
├── .env.example           ← API key template
├── requirements.txt
├── modules/
│   ├── __init__.py
│   ├── groq_client.py     ← Groq API wrapper
│   ├── resume_parser.py   ← PDF + text parsing
│   ├── job_fetcher.py     ← LinkedIn URL scraper
│   └── prompt_builder.py  ← Prompt assembly logic
└── utils/
    ├── __init__.py
    └── helpers.py         ← Formatting & copy helpers

# ── App Meta ─────────────────────────────────────────────────

APP_TITLE: str = "Apply-AI ✍️"

APP_SUBTITLE: str = "Generate tailored cover letters & cold emails in seconds"

APP_VERSION: str = "1.0.0"
