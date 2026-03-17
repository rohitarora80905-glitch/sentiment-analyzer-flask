# SentimentLens — Sentiment Analysis Web App

A full-stack NLP web app that analyzes the emotional tone of any text using lexicon-based sentiment analysis with negation handling and intensifier detection.

## Features
- Real-time sentiment analysis (Positive / Negative / Neutral)
- Confidence score with animated ring indicator
- Positive/Negative/Neutral score breakdown with animated bars
- Negation handling ("not good" → negative)
- Intensifier detection ("very bad" → stronger negative)
- Keyword highlighting (matched sentiment words)
- Word count & sentence count stats
- Example text presets

## Tech Stack
- **Backend**: Python, Flask, Flask-CORS
- **Frontend**: HTML, CSS, Vanilla JavaScript
- **NLP**: Custom lexicon-based analysis (no heavy ML libraries needed)

## Setup & Run

```bash
# 1. Install dependencies
pip install flask flask-cors

# 2. Run the server
python app.py

# 3. Open in browser
# http://localhost:5000
```

## Project Structure
```
sentiment-analyzer/
├── app.py              # Flask backend with NLP logic
├── static/
│   └── index.html      # Frontend UI
├── requirements.txt
└── README.md
```

## How It Works
1. User inputs text in the browser
2. Frontend POSTs text to `/analyze` endpoint
3. Backend tokenizes text, scans each word against lexicons
4. Handles negation (3-word window before each word)
5. Applies intensifier multipliers (very, extremely, etc.)
6. Returns compound score, label, and matched keywords
7. Frontend renders animated result cards

## API Endpoints
- `POST /analyze` — Analyze single text `{ "text": "..." }`
- `POST /batch` — Analyze multiple texts `{ "texts": [...] }`

## Resume Talking Points
- Built a full-stack NLP pipeline from scratch without ML frameworks
- Implemented negation handling and intensifier detection in custom tokenizer
- Designed a REST API with Flask and consumed it with Vanilla JS
- Created animated data visualizations (confidence ring, score bars) in pure CSS/JS
