# JobShield AI - System Architecture

## Overview

JobShield AI is a comprehensive recruitment fraud detection system that combines machine learning, rule-based detection, company verification, and behavioral analysis to identify job scams across multiple communication channels.

## System Components

### 1. Input Ingestion Layer

**Purpose**: Normalize and standardize input from multiple sources

**Supported Channels**:
- Email body text
- WhatsApp messages
- Telegram chats
- Job description snippets
- OCR-extracted text (future enhancement)

**Implementation**: `app.py` - `/analyze` endpoint

### 2. NLP Preprocessing Pipeline

**Purpose**: Clean and prepare text for analysis

**Components**:
- Unicode normalization
- URL/phone/email removal
- Stopword filtering
- Lemmatization
- Feature extraction

**Implementation**: `utils/text_preprocessor.py`

**Key Features**:
- Urgency score calculation
- Payment indicator detection
- Promise pattern recognition

### 3. ML Classification Engine

**Purpose**: Statistical scam detection using supervised learning

**Models Trained**:
1. Logistic Regression (baseline)
2. Decision Tree (interpretable)
3. K-Nearest Neighbors (similarity-based)
4. Random Forest (ensemble)
5. Gradient Boosting (best performance)

**Implementation**: `models/ml_classifier.py`

**Features**:
- TF-IDF vectorization (1000 features, bigrams)
- 5-fold cross-validation
- Automatic best model selection
- Probability calibration

**Training Data**: `data/sample_dataset.py` (30 samples - expandable)

### 4. Rule-Based Fraud Engine

**Purpose**: Deterministic detection of known scam patterns

**Rule Categories**:
- Payment requests (severity: 30)
- Instant offers (severity: 20)
- Urgency tactics (severity: 15)
- Suspicious contact methods (severity: 20)
- Unrealistic salary promises (severity: 15)

**Implementation**: `utils/fraud_rules.py`

**Output**:
- Triggered rules list
- Aggregate rule score (0-100)
- High-confidence scam flag (score ≥ 50)

### 5. Company Legitimacy Verification

**Purpose**: Validate company existence and authenticity

**Data Sources**:
- OpenCorporates API (primary)
- Email domain analysis (secondary)

**Implementation**: `utils/company_verifier.py`

**Verification Checks**:
- Company registry lookup
- Name matching confidence
- Active/inactive status
- Incorporation date validation
- Email domain-company name consistency

**Output**:
- Company found (boolean)
- Confidence score (0-100)
- Company metadata (name, jurisdiction, status)

### 6. Salary Anomaly Detection

**Purpose**: Identify unrealistic compensation offers

**Methodology**:
- Market benchmark comparison
- Z-score deviation analysis
- Job level classification

**Implementation**: `utils/salary_analyzer.py`

**Benchmarks** (in thousands/year):
- Entry: 300-600k (median: 400k)
- Junior: 400-800k (median: 600k)
- Mid: 600-1500k (median: 1000k)
- Senior: 1200-3000k (median: 2000k)
- Lead: 2000-5000k (median: 3000k)

**Anomaly Thresholds**:
- High anomaly: >150% of max benchmark
- Moderate anomaly: >100% of max benchmark

### 7. Recruiter Trust Scoring

**Purpose**: Assess recruiter credibility

**Scoring Factors**:
- Email domain credibility (-20 to +20)
- Contact method legitimacy (-25 to +15)
- LinkedIn profile presence (-10 to +20)

**Implementation**: `utils/recruiter_scorer.py`

**Trust Levels**:
- HIGH_TRUST: ≥70%
- MODERATE_TRUST: 50-69%
- LOW_TRUST: 30-49%
- UNTRUSTED: <30%

### 8. Risk Fusion Engine

**Purpose**: Combine multiple signals into unified fraud score

**Component Weights**:
- ML probability: 35%
- Rule score: 25%
- Company verification: 20%
- Salary anomaly: 10%
- Recruiter trust: 10%

**Implementation**: `utils/risk_fusion.py`

**Risk Tiers**:
- CRITICAL_FRAUD: ≥75%
- HIGH_SCAM_LIKELIHOOD: 50-74%
- MODERATE_RISK: 30-49%
- LOW_RISK: <30%

**Recommendations**:
- Critical: "IGNORE - Report immediately"
- High: "AVOID - Strong fraud indicators"
- Moderate: "PROCEED WITH CAUTION"
- Low: "SAFE TO PROCEED"

### 9. Explainable AI Module

**Purpose**: Provide transparent, interpretable results

**Explanation Types**:
- ML model confidence
- Triggered fraud patterns
- Company verification failures
- Salary anomalies
- Recruiter credibility issues

**Implementation**: `utils/risk_fusion.py` - `get_explanation()`

**Output Format**:
```python
{
    'factor': 'Risk Factor Name',
    'severity': 'high|medium|low',
    'detail': 'Human-readable explanation'
}
```

### 10. Forensic Report Generator

**Purpose**: Generate comprehensive PDF analysis reports

**Implementation**: `utils/pdf_generator.py`

**Report Sections**:
1. Report metadata (timestamp, ID)
2. Risk score summary
3. Recommendation
4. Component breakdown
5. Evidence and explanations
6. Triggered fraud patterns
7. Company verification results
8. Salary analysis
9. Recruiter trust score
10. Original job posting content

**Technology**: ReportLab library

### 11. Web Dashboard

**Purpose**: Interactive user interface

**Implementation**:
- Backend: Flask (`app.py`)
- Frontend: HTML/CSS/JS (`templates/`, `static/`)
- Styling: Bootstrap 5
- Icons: Font Awesome

**Features**:
- Real-time analysis
- Quick test samples
- Visual risk indicators
- PDF report download
- Model training interface

## Data Flow

```
User Input (Job Posting)
    ↓
Text Preprocessing
    ↓
┌─────────────────────────────────────┐
│  Parallel Analysis Pipelines        │
├─────────────────────────────────────┤
│ 1. ML Classification                │
│ 2. Rule-Based Detection             │
│ 3. Company Verification             │
│ 4. Salary Anomaly Detection         │
│ 5. Recruiter Trust Scoring          │
└─────────────────────────────────────┘
    ↓
Risk Fusion Engine
    ↓
Explainable AI Module
    ↓
┌─────────────────────────────────────┐
│  Output Generation                  │
├─────────────────────────────────────┤
│ • Risk Score & Tier                 │
│ • Recommendation                    │
│ • Evidence & Explanations           │
│ • PDF Forensic Report               │
└─────────────────────────────────────┘
    ↓
User Dashboard Display
```

## API Architecture

### REST Endpoints

**POST /analyze**
- Input: Job posting data (JSON)
- Output: Complete fraud analysis (JSON)
- Processing time: 2-5 seconds

**POST /train**
- Input: None (uses sample dataset)
- Output: Training results (JSON)
- Processing time: 10-30 seconds

**GET /download/<filename>**
- Input: PDF filename
- Output: PDF file download

**GET /health**
- Input: None
- Output: System health status

## Security Considerations

1. **Input Validation**: All user inputs sanitized
2. **API Rate Limiting**: Recommended for production
3. **PII Handling**: No storage of personal data
4. **API Keys**: Environment variable configuration
5. **HTTPS**: Required for production deployment

## Scalability

### Current Limitations
- Single-threaded Flask server
- In-memory model storage
- Synchronous processing

### Production Enhancements
- Gunicorn/uWSGI deployment
- Redis caching for API responses
- Celery for async processing
- PostgreSQL for scam repository
- Load balancing for high traffic

## Performance Metrics

### ML Model Performance (Sample Dataset)
- Precision: ~85-95%
- Recall: ~80-90%
- F1-Score: ~85-92%
- ROC-AUC: ~0.90-0.95

### System Performance
- Analysis time: 2-5 seconds
- PDF generation: 1-2 seconds
- API response time: <5 seconds

## Future Enhancements

1. **Deep Learning Models**
   - BERT/RoBERTa for better NLP
   - Transformer-based classification

2. **Enhanced Verification**
   - LinkedIn API integration (official)
   - Domain age checking
   - SSL certificate validation

3. **Multi-language Support**
   - Hindi, Tamil, Telugu support
   - Regional scam pattern detection

4. **Real-time Monitoring**
   - Browser extension
   - Mobile app integration
   - Email plugin

5. **Collaborative Intelligence**
   - User-reported scams database
   - Community-driven pattern updates
   - Federated learning

## Technology Stack

- **Backend**: Python 3.8+, Flask
- **ML/NLP**: scikit-learn, NLTK, XGBoost
- **PDF**: ReportLab
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **APIs**: OpenCorporates
- **Deployment**: Flask dev server (production: Gunicorn)

## License

MIT License - Open source for educational and commercial use
