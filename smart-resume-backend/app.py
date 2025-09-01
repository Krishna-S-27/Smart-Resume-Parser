import os
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from src.extract_text import extract_text_from_upload
from src.preprocess import clean_text
from src.ai_parser import parse_resume_with_ai
from src.exporter import save_json, save_csv, get_json_path, get_csv_path

app = FastAPI(
    title="Smart Resume Parser (AI-powered)",
    description="Upload resumes (PDF/DOCX) → Extract structured data & AI score",
    version="2.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
def ping():
    return {"message": "pong"}


@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    filename = file.filename or ""
    if not filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(status_code=400, detail="Only PDF or DOCX supported.")

    file_bytes = await file.read()

    # Step 1: Extract text
    raw_text = extract_text_from_upload(filename, file_bytes)
    if not raw_text.strip():
        raise HTTPException(status_code=422, detail="No text found in file.")

    # Step 2: Clean text
    text = clean_text(raw_text)

    # Step 3: Parse with AI
    try:
        parsed = parse_resume_with_ai(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail="AI parsing error: " + str(e))

    # Step 5: Save results
    export_id = uuid.uuid4().hex
    try:
        save_json(parsed, export_id)
        save_csv(parsed, export_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Save error: " + str(e))

    return JSONResponse(
        content={
            "status": "success",
            "message": "Resume parsed & scored successfully",
            "export_id": export_id,
            "downloads": {
                "json": "/download/json/" + export_id,
                "csv": "/download/csv/" + export_id,
            },
            "data": parsed,
            
        }
    )


@app.get("/download/json/{export_id}")
def download_json(export_id):
    path = get_json_path(export_id)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="JSON not found")
    return FileResponse(path, media_type="application/json", filename="resume_" + export_id + ".json")


@app.get("/download/csv/{export_id}")
def download_csv(export_id):
    path = get_csv_path(export_id)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="CSV not found")
    return FileResponse(path, media_type="text/csv", filename="resume_" + export_id + ".csv")
