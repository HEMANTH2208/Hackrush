# JobShield AI - Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/HEMANTH2208/Hackrush.git
cd Hackrush
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download NLTK Data

```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"
```

### 5. Configure Environment Variables (Optional)

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Edit `.env`:
```
OPENCORPORATES_API_KEY=your_api_key_here
FLASK_SECRET_KEY=your_secret_key_here
```

Note: OpenCorporates API key is optional. The system works without it but with limited company verification.

### 6. Train ML Models

```bash
python train_models.py
```

This will train multiple ML classifiers and save the best model.

### 7. Run the Application

```bash
python app.py
```

The application will start at `http://localhost:5000`

## Quick Start

1. Open your browser and navigate to `http://localhost:5000`
2. Click "Train Models" button (if not done via command line)
3. Try the quick test samples or paste your own job posting
4. Click "Analyze for Fraud"
5. View results and download PDF report

## Project Structure

```
JobShield/
├── app.py                      # Flask application
├── train_models.py             # Model training script
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── models/
│   ├── ml_classifier.py       # ML classification models
│   └── saved/                 # Trained model files
├── utils/
│   ├── text_preprocessor.py   # Text preprocessing
│   ├── fraud_rules.py         # Rule-based detection
│   ├── salary_analyzer.py     # Salary anomaly detection
│   ├── company_verifier.py    # Company verification
│   ├── recruiter_scorer.py    # Recruiter trust scoring
│   ├── risk_fusion.py         # Risk score fusion
│   └── pdf_generator.py       # PDF report generation
├── data/
│   └── sample_dataset.py      # Training dataset
├── templates/
│   └── index.html             # Web interface
├── static/
│   ├── css/
│   │   └── style.css          # Styling
│   └── js/
│       └── app.js             # Frontend logic
└── reports/                   # Generated PDF reports
```

## Features

### 1. Multi-Channel Input Support
- Email body text
- WhatsApp/Telegram messages
- Job description snippets

### 2. NLP-Driven Classification
- TF-IDF vectorization
- Multiple ML models (Logistic Regression, Decision Tree, KNN, Random Forest, Gradient Boosting)
- Cross-validation and model selection

### 3. Rule-Based Detection
- Payment request patterns
- Instant offer indicators
- Urgency signals
- Suspicious contact methods

### 4. Company Verification
- OpenCorporates API integration
- Email domain validation
- Company existence confidence scoring

### 5. Salary Anomaly Detection
- Market benchmark comparison
- Z-score deviation analysis
- Job level classification

### 6. Recruiter Trust Scoring
- Email domain credibility
- Contact method analysis
- LinkedIn profile validation

### 7. Risk Fusion Engine
- Multi-factor risk scoring
- Weighted component fusion
- Risk tier classification

### 8. Explainable AI
- Evidence highlighting
- Factor-based explanations
- Transparent decision making

### 9. PDF Report Generation
- Comprehensive forensic reports
- Risk assessment summary
- Evidence documentation

## API Endpoints

### POST /analyze
Analyze job posting for fraud

Request:
```json
{
  "job_text": "Job description...",
  "company_name": "Company Name",
  "recruiter_email": "email@example.com",
  "contact_method": "email",
  "linkedin_url": "https://linkedin.com/in/...",
  "offered_salary": 1200
}
```

Response:
```json
{
  "risk_score": 75.5,
  "risk_tier": "HIGH_SCAM_LIKELIHOOD",
  "recommendation": "AVOID - Strong indicators of fraud",
  "component_scores": {...},
  "explanations": [...],
  "pdf_report": "fraud_analysis_20240115_123456.pdf"
}
```

### POST /train
Train ML models with sample data

### GET /health
Health check endpoint

### GET /download/<filename>
Download PDF report

## Troubleshooting

### NLTK Data Not Found
```bash
python -c "import nltk; nltk.download('all')"
```

### Port Already in Use
Change port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Models Not Loading
Run training script:
```bash
python train_models.py
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

MIT License

## Support

For issues and questions, please open an issue on GitHub.
