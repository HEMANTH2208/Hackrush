# JobShield AI - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Clone the Repository
```bash
git clone https://github.com/HEMANTH2208/Hackrush.git
cd Hackrush
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Download NLTK Data
```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"
```

### Step 4: Train Models
```bash
python train_models.py
```

### Step 5: Run the Application
```bash
python app.py
```

### Step 6: Open Browser
Navigate to: **http://localhost:5000**

---

## 🎯 Quick Test

### Test with Scam Example
1. Click "Load Scam Example" button
2. Click "Analyze for Fraud"
3. See high risk score (75-95%)
4. Download PDF report

### Test with Legitimate Example
1. Click "Load Legitimate Example" button
2. Click "Analyze for Fraud"
3. See low risk score (10-30%)
4. Compare results

---

## 📋 What You'll See

### Risk Score Dashboard
- **Risk Score**: 0-100% fraud probability
- **Risk Tier**: CRITICAL/HIGH/MODERATE/LOW
- **Recommendation**: Action to take

### Analysis Components
1. **ML Model Detection**: AI-based classification
2. **Fraud Pattern Matches**: Rule-based triggers
3. **Risk Factors**: Explainable evidence
4. **Company Verification**: Registry lookup results
5. **Salary Analysis**: Market comparison
6. **Recruiter Trust**: Credibility assessment

### PDF Report
- Comprehensive forensic analysis
- Evidence documentation
- Professional format
- Downloadable and shareable

---

## 🔧 Troubleshooting

### Issue: Models not loading
**Solution**: Run `python train_models.py`

### Issue: NLTK data not found
**Solution**: 
```bash
python -c "import nltk; nltk.download('all')"
```

### Issue: Port 5000 already in use
**Solution**: Edit `app.py` and change port:
```python
app.run(debug=True, port=5001)
```

### Issue: OpenCorporates API errors
**Solution**: Company verification works without API key (limited functionality)

---

## 📊 Sample Inputs

### Scam Example
```
Congratulations! You are selected for Google. 
Salary 25 LPA for freshers. Pay Rs 5000 registration 
fee to confirm your joining within 24 hours. 
Contact via WhatsApp only: +91-9876543210
```

### Legitimate Example
```
We are pleased to inform you that your application 
for Software Engineer position has been shortlisted. 
We would like to invite you for an interview at our 
Bangalore office on 25th January at 10:00 AM. 
Please bring your resume and certificates.
```

---

## 🎓 Understanding Results

### Risk Tiers

**🔴 CRITICAL FRAUD (75-100%)**
- Multiple scam indicators
- High confidence fraud
- Action: IGNORE and REPORT

**🟠 HIGH SCAM LIKELIHOOD (50-74%)**
- Strong fraud signals
- Likely scam
- Action: AVOID

**🟡 MODERATE RISK (30-49%)**
- Some suspicious elements
- Requires verification
- Action: PROCEED WITH CAUTION

**🟢 LOW RISK (0-29%)**
- Minimal fraud indicators
- Likely legitimate
- Action: SAFE TO PROCEED

---

## 🛠️ Advanced Usage

### Train with Custom Data
Edit `data/sample_dataset.py` and add your samples:
```python
TRAINING_DATA = [
    ("Your scam text here", 1),  # 1 = scam
    ("Your legit text here", 0),  # 0 = legitimate
    # Add more...
]
```

Then retrain:
```bash
python train_models.py
```

### Configure API Keys
Create `.env` file:
```
OPENCORPORATES_API_KEY=your_key_here
FLASK_SECRET_KEY=your_secret_key
```

### Deploy to Production
Use Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 📚 Documentation

- **README.md**: Project overview
- **SETUP.md**: Detailed installation guide
- **ARCHITECTURE.md**: System design and components
- **QUICKSTART.md**: This file

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

---

## 📞 Support

- **GitHub Issues**: Report bugs and request features
- **Email**: Contact repository owner
- **Documentation**: Check SETUP.md and ARCHITECTURE.md

---

## ⭐ Features Checklist

- ✅ Multi-channel input support
- ✅ NLP preprocessing pipeline
- ✅ Multiple ML classifiers
- ✅ Rule-based fraud detection
- ✅ Company verification (OpenCorporates)
- ✅ Salary anomaly detection
- ✅ Recruiter trust scoring
- ✅ Risk fusion engine
- ✅ Explainable AI
- ✅ PDF report generation
- ✅ Interactive web dashboard
- ✅ Quick test samples
- ✅ Model training interface

---

## 🏆 Hackathon Ready

This project is fully functional and demo-ready:
- ✅ Complete end-to-end system
- ✅ Professional UI/UX
- ✅ Explainable results
- ✅ PDF reports
- ✅ Sample data included
- ✅ Easy deployment
- ✅ Comprehensive documentation

---

## 📄 License

MIT License - Free for educational and commercial use

---

**Happy Fraud Detection! 🛡️**
