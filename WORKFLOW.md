# JobShield AI - System Workflow

## Visual System Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER INPUT LAYER                            │
│  📧 Email  |  💬 WhatsApp  |  📱 Telegram  |  📄 Job Posting   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                  TEXT PREPROCESSING                             │
│  • Unicode Normalization                                        │
│  • URL/Phone/Email Removal                                      │
│  • Stopword Filtering                                           │
│  • Lemmatization                                                │
│  • Feature Extraction (urgency, payment, promises)              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│              PARALLEL ANALYSIS PIPELINES                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐                   │
│  │  ML CLASSIFIER   │  │  RULE ENGINE     │                   │
│  │  • Logistic Reg  │  │  • Payment       │                   │
│  │  • Decision Tree │  │  • Instant Offer │                   │
│  │  • KNN           │  │  • Urgency       │                   │
│  │  • Random Forest │  │  • Contact       │                   │
│  │  • Gradient Boost│  │  • Salary        │                   │
│  │  ↓ Probability   │  │  ↓ Rule Score    │                   │
│  └──────────────────┘  └──────────────────┘                   │
│                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐                   │
│  │  COMPANY VERIFY  │  │  SALARY ANALYZER │                   │
│  │  • OpenCorporates│  │  • Market Range  │                   │
│  │  • Registry Check│  │  • Z-Score       │                   │
│  │  • Email Domain  │  │  • Job Level     │                   │
│  │  ↓ Confidence    │  │  ↓ Anomaly Score │                   │
│  └──────────────────┘  └──────────────────┘                   │
│                                                                 │
│  ┌──────────────────┐                                          │
│  │ RECRUITER SCORER │                                          │
│  │  • Email Domain  │                                          │
│  │  • Contact Method│                                          │
│  │  • LinkedIn      │                                          │
│  │  ↓ Trust Score   │                                          │
│  └──────────────────┘                                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   RISK FUSION ENGINE                            │
│                                                                 │
│  Weighted Scoring:                                              │
│  • ML Probability      (35%)  ────┐                            │
│  • Rule Score          (25%)  ────┤                            │
│  • Company Confidence  (20%)  ────┼──→  UNIFIED RISK SCORE     │
│  • Salary Anomaly      (10%)  ────┤      (0-100%)              │
│  • Recruiter Trust     (10%)  ────┘                            │
│                                                                 │
│  Risk Tier Classification:                                      │
│  🔴 CRITICAL (75-100%)  →  IGNORE & REPORT                     │
│  🟠 HIGH (50-74%)       →  AVOID                               │
│  🟡 MODERATE (30-49%)   →  PROCEED WITH CAUTION                │
│  🟢 LOW (0-29%)         →  SAFE TO PROCEED                     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   EXPLAINABLE AI MODULE                         │
│                                                                 │
│  Evidence Generation:                                           │
│  • Suspicious phrase highlighting                              │
│  • Feature importance extraction                               │
│  • Factor-based explanations                                   │
│  • Severity classification                                     │
│                                                                 │
│  Example Output:                                                │
│  ✗ Company not found in registry (HIGH)                        │
│  ✗ Payment request detected: "pay Rs 5000" (HIGH)              │
│  ✗ Salary 150% above market rate (MEDIUM)                      │
│  ✗ Using WhatsApp only contact (MEDIUM)                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    OUTPUT GENERATION                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────────┐         ┌────────────────────┐         │
│  │  WEB DASHBOARD     │         │  PDF REPORT        │         │
│  │  • Risk Score      │         │  • Forensic Report │         │
│  │  • Risk Tier       │         │  • Evidence Docs   │         │
│  │  • Recommendation  │         │  • Component Scores│         │
│  │  • Component Scores│         │  • Original Content│         │
│  │  • Evidence List   │         │  • Downloadable    │         │
│  │  • Visual Charts   │         │  • Professional    │         │
│  └────────────────────┘         └────────────────────┘         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      USER ACTION                                │
│  Based on risk tier and recommendation:                         │
│  • IGNORE and report to authorities                             │
│  • AVOID the opportunity                                        │
│  • VERIFY independently before proceeding                       │
│  • PROCEED with standard caution                                │
└─────────────────────────────────────────────────────────────────┘
```

## Component Interaction Diagram

```
┌──────────────┐
│   Flask App  │
│   (app.py)   │
└──────┬───────┘
       │
       ├─────────────────────────────────────────────────┐
       │                                                 │
       ↓                                                 ↓
┌──────────────┐                                 ┌──────────────┐
│  Frontend    │                                 │   Backend    │
│  (HTML/JS)   │◄────────JSON Response───────────│   Routes     │
└──────────────┘                                 └──────┬───────┘
                                                        │
       ┌────────────────────────────────────────────────┼────────────────┐
       │                    │                           │                │
       ↓                    ↓                           ↓                ↓
┌─────────────┐      ┌─────────────┐          ┌─────────────┐   ┌─────────────┐
│Text Preproc │      │ML Classifier│          │Rule Engine  │   │Salary Analyz│
│(utils/)     │      │(models/)    │          │(utils/)     │   │(utils/)     │
└─────────────┘      └─────────────┘          └─────────────┘   └─────────────┘
       │                    │                           │                │
       └────────────────────┼───────────────────────────┼────────────────┘
                            │                           │
                            ↓                           ↓
                     ┌─────────────┐          ┌─────────────┐
                     │Company Verif│          │Recruiter Scr│
                     │(utils/)     │          │(utils/)     │
                     └──────┬──────┘          └──────┬──────┘
                            │                        │
                            └────────┬───────────────┘
                                     │
                                     ↓
                            ┌─────────────┐
                            │Risk Fusion  │
                            │(utils/)     │
                            └──────┬──────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
                    ↓                             ↓
            ┌─────────────┐              ┌─────────────┐
            │Explainable  │              │PDF Generator│
            │AI (utils/)  │              │(utils/)     │
            └─────────────┘              └─────────────┘
```

## Data Flow Timeline

```
Time: 0ms
├─ User submits job posting
│
Time: 100ms
├─ Text preprocessing complete
│  └─ Cleaned text, extracted features
│
Time: 500ms
├─ ML classification complete
│  └─ Scam probability: 85%
│
Time: 800ms
├─ Rule engine complete
│  └─ 3 patterns matched, score: 65
│
Time: 2000ms
├─ Company verification complete
│  └─ Not found in registry
│
Time: 2200ms
├─ Salary analysis complete
│  └─ 150% above market rate
│
Time: 2300ms
├─ Recruiter scoring complete
│  └─ Trust score: 25% (UNTRUSTED)
│
Time: 2500ms
├─ Risk fusion complete
│  └─ Final score: 78% (CRITICAL)
│
Time: 3000ms
├─ Explainable AI complete
│  └─ 5 risk factors identified
│
Time: 4000ms
├─ PDF report generated
│  └─ fraud_analysis_20240115_123456.pdf
│
Time: 4500ms
└─ Results displayed to user
   └─ Dashboard + Download link
```

## API Request/Response Flow

### Request
```http
POST /analyze HTTP/1.1
Content-Type: application/json

{
  "job_text": "Congratulations! Pay Rs 5000...",
  "company_name": "Google",
  "recruiter_email": "hr@gmail.com",
  "contact_method": "whatsapp",
  "offered_salary": 2500
}
```

### Processing Steps
```
1. Validate input
2. Preprocess text
3. Run parallel analyses:
   - ML classification
   - Rule matching
   - Company verification
   - Salary analysis
   - Recruiter scoring
4. Fuse risk signals
5. Generate explanations
6. Create PDF report
7. Return JSON response
```

### Response
```json
{
  "risk_score": 78.5,
  "risk_tier": "CRITICAL_FRAUD",
  "recommendation": "IGNORE - Report immediately",
  "component_scores": {
    "ml_probability": 85.0,
    "rule_score": 65.0,
    "company_risk": 100.0,
    "salary_anomaly": 75.0,
    "recruiter_risk": 75.0
  },
  "explanations": [
    {
      "factor": "Company Verification Failed",
      "severity": "high",
      "detail": "Company not found in registry"
    }
  ],
  "pdf_report": "fraud_analysis_20240115_123456.pdf"
}
```

## User Journey

```
1. User receives suspicious job offer
   ↓
2. Opens JobShield AI dashboard
   ↓
3. Pastes job text and fills details
   ↓
4. Clicks "Analyze for Fraud"
   ↓
5. System processes (2-5 seconds)
   ↓
6. Results displayed with:
   - Risk score (color-coded)
   - Risk tier badge
   - Recommendation
   - Component breakdown
   - Evidence list
   ↓
7. User downloads PDF report
   ↓
8. User takes action based on recommendation
```

## Error Handling Flow

```
Input Validation
    ↓
    ├─ Valid → Continue
    └─ Invalid → Return 400 error
         ↓
Text Preprocessing
    ↓
    ├─ Success → Continue
    └─ Error → Use raw text
         ↓
ML Classification
    ↓
    ├─ Model loaded → Predict
    └─ No model → Use default (50%)
         ↓
External API Calls
    ↓
    ├─ Success → Use results
    └─ Timeout/Error → Use fallback values
         ↓
Risk Fusion
    ↓
    ├─ All signals → Calculate
    └─ Missing signals → Use defaults
         ↓
PDF Generation
    ↓
    ├─ Success → Return path
    └─ Error → Log and continue
         ↓
Return Results (always succeeds)
```

## Deployment Flow

```
Development
    ↓
├─ Local testing with Flask dev server
├─ Model training with sample data
└─ Feature validation
    ↓
Staging
    ↓
├─ Gunicorn WSGI server
├─ Nginx reverse proxy
└─ SSL certificate
    ↓
Production
    ↓
├─ Docker containerization
├─ Kubernetes orchestration
├─ Load balancing
├─ Auto-scaling
└─ Monitoring & logging
```

---

**This workflow ensures reliable, explainable, and fast fraud detection for job seekers.**
