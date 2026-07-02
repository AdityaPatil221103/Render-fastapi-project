from fastapi import FastAPI, UploadFile, File,HTTPException
from fastapi.staticfiles import StaticFiles
import os 
import shutil

app = FastAPI()

#step1: ensure uploads folders exists

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

#step2:static file setup
#URL: HTTP://127.0.0.:8080/FILES/<FILENAME>

app.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="files")

#step3:Uplaod file
@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    filename = file.filename
    file_path = os.path.join(UPLOAD_DIR, filename)

    if not filename:
        raise HTTPException(
            status_code=400,
            detail="File not found"
        )
    with open(file_path,"wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

        return{
            "message":"File Uploaded Successfully",
            "filename":filename,
            "file_url": f"http://127.0.0.1:8000/files/{filename}"
        }
    
#step4: Get the file URL API

@app.get("/file/{filename}")
def get_file(filename:str):
    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="file not found"
        )
    return{
        "file_url": f"http://127.0.0.1:8000/files/{filename}"
    }

@app.get("/")
def home():
    return{
        "message":"File Uploaded Api running"
    }