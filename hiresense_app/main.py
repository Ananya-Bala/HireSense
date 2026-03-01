from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import shutil
import os
import uuid

from app.resume_processor import extract_text_from_pdf
from app.role_engine import evaluate_role
from app.summary_engine import generate_executive_summary
from data.role_profiles import role_profiles


app = FastAPI(
    title="AI Resume Screening Engine",
    docs_url=None,
    redoc_url=None
)

templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Serve UI
# -----------------------------
@app.get("/", response_class=HTMLResponse)
def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Prevent favicon 404
@app.get("/favicon.ico")
def favicon():
    return {}


# -----------------------------
# Get Available Roles
# -----------------------------
@app.get("/roles")
def get_roles():
    return {"available_roles": list(role_profiles.keys())}


# -----------------------------
# Resume Evaluation Endpoint
# -----------------------------
@app.post("/evaluate")
async def evaluate_resume(
    target_role: str,
    file: UploadFile = File(...)
):
    if target_role not in role_profiles:
        raise HTTPException(status_code=400, detail="Invalid role selected.")

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    temp_filename = f"temp_{uuid.uuid4().hex}.pdf"

    try:
        # Save uploaded file temporarily
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract text
        resume_text = extract_text_from_pdf(temp_filename)

        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF.")

        # Structured evaluation
        structured_result = evaluate_role(
            resume_text=resume_text,
            role_name=target_role,
            similarity_score=0.5  # Default similarity score
        )

        # Deterministic executive summary
        structured_result["analysis_summary"] = generate_executive_summary(
            structured_result
        )

        return structured_result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)