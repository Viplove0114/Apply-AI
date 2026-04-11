# Apply-AI ✍️

> Generate tailored cover letters & cold emails in seconds — powered by Groq's LLaMA 3.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red?logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/LLM-Groq%20LLaMA%203-green)

---

## ✨ Features

- 📋 **Paste or Upload** — Provide your resume as text or upload a PDF
- 🔗 **LinkedIn Scraping** — Paste a LinkedIn post URL to auto-extract the job description
- 🎭 **6 Tone Options** — Professional, Warm, Confident, Casual, Formal, Creative
- 📏 **Output Length Control** — Small (~250 words) or Large (~500 words)
- 🤖 **Humanized Output** — Specifically prompted to avoid AI-sounding language
- 📧 **Cover Letters & Cold Emails** — Switch between formats instantly

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/apply-ai.git
cd apply-ai
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

```bash
cp .env.example .env
# Edit .env and add your Groq API key
# Get a free key at: https://console.groq.com/keys
```

### 5. Run the app

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
apply-ai/
├── app.py                 ← Streamlit UI entry point
├── config.py              ← All constants & settings
├── .env.example           ← API key template
├── .gitignore
├── requirements.txt
├── README.md
├── modules/
│   ├── __init__.py
│   ├── groq_client.py     ← Groq API wrapper
│   ├── resume_parser.py   ← PDF + text parsing
│   ├── job_fetcher.py     ← LinkedIn URL scraper
│   └── prompt_builder.py  ← Prompt assembly logic
└── utils/
    ├── __init__.py
    └── helpers.py          ← Formatting & copy helpers
```

---

## 🎭 Tone Options

| Tone                   | Description                                     |
| ---------------------- | ----------------------------------------------- |
| **Professional** | Polished and business-appropriate               |
| **Warm**         | Friendly and approachable with a personal touch |
| **Confident**    | Assertive, leading with accomplishments         |
| **Casual**       | Conversational, like talking to a peer          |
| **Formal**       | Traditional business writing conventions        |
| **Creative**     | Unique, memorable, slightly unconventional      |

---

## 🔑 Getting a Groq API Key

1. Visit [console.groq.com/keys](https://console.groq.com/keys)
2. Sign up for a free account
3. Create a new API key
4. Add it to your `.env` file

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **LLM**: Groq API (LLaMA 3.3 70B Versatile, openai/gpt-oss-120b)
- **PDF Parsing**: PyPDF2
- **Web Scraping**: requests + BeautifulSoup4 + lxml
- **Config**: python-dotenv

---

## 🚀 Future Improvements

Here are some exciting features planned for upcoming versions:

| #  | Feature                               | Description                                                                                              |
| -- | ------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| 1  | 🧠**AI Interview Prep**         | Generate tailored interview Q&A based on the job description and your resume — practice before the call |
| 2  | 📊**Resume-JD Match Score**     | Show a compatibility percentage between your resume and the job description with skill gap analysis      |
| 3  | 🔄**Multi-Version Generator**   | Generate 3 different versions at once (different tones) so you can pick the best one                     |
| 4  | 💾**History & Templates**       | Save previously generated emails/letters and reuse them as templates for similar roles                   |
| 5  | 🌐**Chrome Extension**          | A browser extension that auto-detects job posts on LinkedIn and generates emails with one click          |
| 6  | 📧**Direct Email Integration**  | Connect with Gmail / Outlook API to send the generated email directly from the app                       |
| 7  | 🧩**Multiple LLM Support**      | Add support for OpenAI, Anthropic, and Gemini models — let the user pick their preferred LLM            |
| 8  | 📝**Follow-Up Email Generator** | Generate professional follow-up emails if you haven't heard back after X days                            |
| 9  | 🎯**Keyword Optimization**      | Highlight ATS-friendly keywords from the JD and ensure they appear naturally in the output               |
| 10 | 🔍**LinkedIn Profile Scraper**  | Auto-import your LinkedIn profile as resume input — no need to paste or upload anything                 |
| 11 | 🌍**Multi-Language Support**    | Generate cover letters and emails in different languages (Hindi, German, French, etc.)                   |
| 12 | 📱**Mobile-Friendly PWA**       | Convert the app into a Progressive Web App for on-the-go usage from your phone                           |

> 💡 **Want to contribute?** Pick any feature above, fork the repo, and submit a PR!

---

## 📄 License

MIT License — feel free to use, modify, and share.
