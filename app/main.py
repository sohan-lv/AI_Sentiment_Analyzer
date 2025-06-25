from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
import os
import nltk

nltk.download('vader_lexicon')

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directory and serve index.html
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    with open("static/index.html") as f:
        return f.read()

# Uploading folder
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-data/")
async def upload_data(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb+") as f:
        f.write(await file.read())

    df = pd.read_csv(file_location)
    return {
        "filename": file.filename,
        "columns": df.columns.tolist(),
        "preview": df.head().to_dict(orient="records")
    }

@app.post("/analyze/")
def analyze_sentiment():
    files = sorted(os.listdir(UPLOAD_DIR), key=lambda x: os.path.getctime(os.path.join(UPLOAD_DIR, x)), reverse=True)

    if not files:
        return {"error": "No file uploaded yet"}

    latest_file = os.path.join(UPLOAD_DIR, files[0])
    df = pd.read_csv(latest_file)

    if "Comment" not in df.columns:
        return {"error": "Column 'Comment' not found in uploaded file."}

    sia = SentimentIntensityAnalyzer()

    df["Sentiment"] = df["Comment"].apply(lambda comment: sia.polarity_scores(comment))
    return df[["Name", "Comment", "Sentiment"]].to_dict(orient="records")
