# JobShield AI

## Explainable Recruitment Scam Detection with Company Legitimacy Verification

JobShield AI is an end-to-end AI-based fraud detection system that identifies recruitment scams across multiple channels (WhatsApp, Email, Telegram) using NLP, machine learning, and company verification.

## Features

- Multi-channel input support (Email, WhatsApp, Telegram)
- NLP-driven scam classification with multiple ML models
- Company legitimacy verification via OpenCorporates API
- Behavioral anomaly detection (salary + urgency patterns)
- Multi-factor risk fusion scoring
- Explainable AI with evidence highlighting
- Automated forensic PDF report generation
- Interactive web dashboard

## Tech Stack

- Backend: Python, Flask
- ML/NLP: scikit-learn, NLTK, Sentence-BERT
- Company Verification: OpenCorporates API
- PDF Generation: ReportLab
- Frontend: HTML, CSS, JavaScript, Bootstrap

## Installation

```bash
pip install -r requirements.txt
python -m nltk.downloader stopwords punkt wordnet
```

## Usage

```bash
python app.py
```

Visit `http://localhost:5000` to access the dashboard.

## Project Structure

```
JobShield/
├── app.py                 # Flask application
├── models/                # ML models and training
├── utils/                 # Utility functions
├── static/                # Frontend assets
├── templates/             # HTML templates
├── data/                  # Training datasets
└── reports/               # Generated PDF reports
```

## License

MIT License
