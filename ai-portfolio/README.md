# 💼 AI Portfolio Assistant

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Powered by Groq](https://img.shields.io/badge/Inference-Groq%20LPU-f55036.svg)](https://groq.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../LICENSE)

An interactive, AI-driven portfolio chatbot built with **FastAPI**, **Groq**, and **modern responsive web tech**. 

Instead of recruiters merely skimming a static PDF, they can converse with an **AI digital twin** of yourself. The bot accurately discusses your technical skills, architectural decisions, project details, and educational background—**strictly grounded in your resume** to avoid hallucinations.

---

## ✨ Features

- 📑 **Multi-Format Resume Ingestion**: Upload `.pdf`, `.pptx`, or `.txt` resumes directly.
- 🤖 **Zero-Hallucination AI Twin**: The LLM prompt strictly bounds responses to resume facts. If an experience or skill is not in your resume, it politely clarifies instead of making things up.
- ⚡ **Ultra-Fast Inference via Groq**: Leverages Groq's high-speed LPU infrastructure with models like `openai/gpt-oss-120b`, `llama-3.3-70b-versatile`, or `llama-3.1-8b-instant`.
- 🔍 **Automated Candidate Profiling**: Automatically detects and extracts candidate name from uploaded resumes to dynamically personalize the UI.
- 💬 **Recruiter-Centric UI**:
  - Sleek modern dark mode interface.
  - Quick-action prompt chips (*Skills*, *Projects*, *Education*, *Contact*).
  - Lightweight Markdown parsing (bullet points, bold emphasis, code blocks).
  - Animated pulsing typing indicator.
  - Session isolation and conversation reset.
- 🔐 **Secured Admin Portal (`/admin`)**: Password-protected dashboard with drag-and-drop file upload to update and re-index resumes anytime.
- 📥 **One-Click Resume Download**: Clean download button automatically activates whenever a resume file is uploaded.
- 🛡️ **Prompt Injection Defense**: Resume content is isolated as passive data, safeguarding against instruction hijacking.

---

## 🏗️ Architecture & Project Structure

```text
ai-portfolio/
├── .env.example            # Sample environment configuration template
├── .gitignore              # Files excluded from git tracking
├── requirements.txt        # Production Python dependencies
├── LICENSE                 # MIT License
├── README.md               # Project documentation
│
└── ai-portfolio/           # Main application directory
    ├── app.py              # FastAPI server, REST API endpoints & CORS middleware
    ├── main.py             # Groq LLM integration, prompt engine & session management
    ├── resume_parser.py    # Robust text extractor for PDF, PPTX, and TXT files
    ├── index.html          # Public recruiter-facing chat application
    ├── admin.html          # Password-protected admin resume upload portal
    ├── .env.example        # Local env template
    └── requirements.txt    # Local dependencies list
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python **3.10** or higher
- A free **Groq API Key** (obtainable from [Groq Console](https://console.groq.com/keys))

### 2. Clone the Repository
```bash
git clone https://github.com/Harshal-Deshmukh/ai-portfolio.git
cd ai-portfolio
```

### 3. Create a Virtual Environment
```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Copy `.env.example` to create your `.env` file:
```bash
cp .env.example .env     # Linux / macOS
copy .env.example .env   # Windows
```

Open `.env` and fill in your values:
```env
# Required: Your Groq API Key
GROQ_API_KEY=gsk_your_actual_groq_api_key_here

# Groq model ID (default: openai/gpt-oss-120b or llama-3.3-70b-versatile)
GROQ_MODEL=openai/gpt-oss-120b

# Secret password for the /admin portal to upload resumes
ADMIN_PASSWORD=change_this_to_a_secure_password

# Fallback candidate name displayed before resume upload
DEFAULT_NAME=Harshal
```

### 6. Run the Application
You can run the application directly using Python or Uvicorn:

```bash
# Option A: Run directly
python app.py

# Option B: Run via Uvicorn with auto-reload
uvicorn app:app --reload --port 8000
```

Open your browser and navigate to:
- **Portfolio Chat**: `http://localhost:8000`
- **Admin Portal**: `http://localhost:8000/admin`
- **API Swagger Docs**: `http://localhost:8000/docs`

---

## 🔐 Admin Portal & Resume Upload

1. Navigate to `http://localhost:8000/admin`.
2. Enter the `ADMIN_PASSWORD` you configured in your `.env`.
3. Drag & drop or select your resume file (`.pdf`, `.pptx`, or `.txt`).
4. Click **Update & Index Resume**.
5. The application extracts the resume text, detects your name via Groq, indexes your profile, and updates the chat engine in real time.

---

## 📡 REST API Reference

| Endpoint | Method | Description | Auth Required |
|---|:---:|---|:---:|
| `/` | `GET` | Serves candidate chat user interface (`index.html`) | None |
| `/admin` | `GET` | Serves admin resume upload dashboard (`admin.html`) | None |
| `/chat` | `POST` | Sends question and returns AI answer | None |
| `/chat/reset` | `POST` | Resets conversation history for session | None |
| `/upload` | `POST` | Uploads and parses `.pdf`, `.pptx`, `.txt` resume | `X-Admin-Password` header |
| `/profile` | `GET` | Returns candidate's detected name | None |
| `/resume/available`| `GET` | Checks if a downloadable resume file exists | None |
| `/resume/download` | `GET` | Downloads the current resume file | None |

---

## 🛡️ Security & Performance Highlights

- **Prompt Injection Hardened**: System prompts treat resume content strictly as read-only data, preventing malicious prompt injections embedded in uploaded documents.
- **Timing-Safe Authentication**: The admin upload endpoint utilizes `secrets.compare_digest` to protect against timing attacks.
- **Session Memory Management**: Conversation history uses an LRU cache with bounded history length to prevent memory exhaustion from long sessions.
- **Client-Side Sanitization**: Chat rendering safely escapes input to mitigate XSS vulnerabilities while parsing lightweight markdown elements.

---

## 📄 License

This project is open-source under the [MIT License](../LICENSE).

---

## 👤 Author

**Harshal Deshmukh**
- GitHub: [@Harshal-Deshmukh](https://github.com/Harshal-Deshmukh)
