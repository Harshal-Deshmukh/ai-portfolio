import os
import secrets
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from main import chat, set_resume, get_name, reset_session
from resume_parser import extract_text

load_dotenv()
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")

BASE_DIR = Path(__file__).parent
MAX_SIZE = 5 * 1024 * 1024  # 5 MB

UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(
    title="AI Portfolio Assistant",
    description="Interactive conversational resume bot built with FastAPI and Groq.",
    version="1.0.0",
)

# Allow CORS for external embedding and cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str
    session_id: str = "default"


class ResetRequest(BaseModel):
    session_id: str = "default"


@app.get("/")
def home():
    return FileResponse(BASE_DIR / "index.html")


@app.get("/admin")
def admin_page():
    return FileResponse(BASE_DIR / "admin.html")


@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    return {"answer": chat(req.question.strip(), req.session_id)}


@app.post("/chat/reset")
def reset_endpoint(req: ResetRequest):
    reset_session(req.session_id)
    return {"status": "ok", "message": "Conversation history cleared."}


@app.post("/upload")
async def upload(file: UploadFile = File(...), x_admin_password: str = Header(default="")):
    if not ADMIN_PASSWORD:
        raise HTTPException(
            status_code=500,
            detail="ADMIN_PASSWORD is not configured on the server. Please set it in your .env file.",
        )

    if not secrets.compare_digest(x_admin_password, ADMIN_PASSWORD):
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid admin password.")

    data = await file.read()
    if len(data) > MAX_SIZE:
        raise HTTPException(status_code=413, detail="File size exceeds the 5 MB limit.")

    try:
        text = extract_text(file.filename, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if len(text.strip()) < 50:
        raise HTTPException(
            status_code=400,
            detail="Insufficient readable text found in document. If this is a scanned PDF, please use a text-based PDF.",
        )

    for old in UPLOAD_DIR.glob("resume.*"):
        try:
            old.unlink()
        except OSError:
            pass

    ext = Path(file.filename).suffix.lower()
    (UPLOAD_DIR / f"resume{ext}").write_bytes(data)

    set_resume(text)
    return {"message": "Resume uploaded and indexed successfully.", "chars": len(text)}


@app.get("/resume/available")
def resume_available():
    return {"available": any(UPLOAD_DIR.glob("resume.*"))}


@app.get("/profile")
def profile():
    return {"name": get_name()}


@app.get("/resume/download")
def download_resume():
    files = list(UPLOAD_DIR.glob("resume.*"))
    if not files:
        raise HTTPException(status_code=404, detail="Resume file is not available.")
    f = files[0]
    safe_name = "".join(c for c in get_name() if c.isalnum() or c in " _-").strip().replace(" ", "_") or "Resume"
    return FileResponse(f, filename=f"{safe_name}_Resume{f.suffix}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)