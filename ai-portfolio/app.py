import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from fastapi.responses import FileResponse
from pydantic import BaseModel

from main import chat, set_resume, get_name
from resume_parser import extract_text

load_dotenv()
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

BASE_DIR = Path(__file__).parent
MAX_SIZE = 5 * 1024 * 1024  # 5 MB

UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI()

class ChatRequest(BaseModel):
    question: str
    session_id: str = "default"

@app.get("/")
def home():
    return FileResponse(BASE_DIR / "index.html")

@app.get("/admin")
def admin_page():
    return FileResponse(BASE_DIR / "admin.html")

@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    return {"answer": chat(req.question, req.session_id)}

@app.post("/upload")
async def upload(file: UploadFile = File(...), x_admin_password: str = Header(default="")):
    if not ADMIN_PASSWORD or x_admin_password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Wrong password")
    data = await file.read()
    if len(data) > MAX_SIZE:
        raise HTTPException(status_code=413, detail="File 5MB se badi hai")
    try:
        text = extract_text(file.filename, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if len(text.strip()) < 50:
        raise HTTPException(status_code=400, detail="Text nahi mila (scanned PDF ho sakti hai)")

    for old in UPLOAD_DIR.glob("resume.*"):
        old.unlink()
    ext = Path(file.filename).suffix.lower()
    (UPLOAD_DIR / f"resume{ext}").write_bytes(data)

    set_resume(text)
    return {"message": "Resume loaded", "chars": len(text)}

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
        raise HTTPException(status_code=404, detail="Resume not available")
    f = files[0]
    safe = "".join(c for c in get_name() if c.isalnum() or c in " _-").strip().replace(" ", "_") or "Resume"
    return FileResponse(f, filename=f"{safe}_Resume{f.suffix}")