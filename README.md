# AI Sentiment Analyzer

This project uses a FastAPI backend and a dynamic HTML frontend to analyze sentiment from uploaded CSV comments. Built for fast and interactive sentiment analysis using VADER.

### Features
- Upload any CSV file with a **Comment** column
- Automated Sentiment Analysis using NLTK’s VADER
- Dynamic bar charts for compound sentiment scores
- Summary metrics (average positive, neutral, negative, and compound)
- Download sentiment-labeled results as CSV

### Tech Stack
- Python (FastAPI)
- VADER Sentiment Analysis
- HTML/CSS/JS (Vanilla)
- Chart.js

### Setup

pip install -r requirements.txt
uvicorn main:app --reload
URL in browser: http://127.0.0.1:8000/static/index.html
