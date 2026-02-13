# JobShield AI - Testing Guide

## 🧪 Complete Testing Checklist

### Prerequisites
```bash
# Ensure you're in the project directory
cd Hackrush

# Install dependencies (if not already done)
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"
```

---

## 1. Initial Setup Test

### Start the Application
```bash
python app.py
```

**Expected Output:**
```
Models loaded: Decision Tree
==================================================
JobShield AI - Recruitment Scam Detection System
==================================================

Starting server...
Access dashboard at: http://localhost:5000

Note: Train models first by clicking 'Train Models' button
==================================================
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Open Browser
1. Navigate to: `http://localhost:5000`
2. **Expected**: Beautiful gradient hero section with statistics
3. **Expected**: Setup alert at top with "Train Models" button
4. **Expected**: Two-column layout (form on left, placeholder on right)

---

## 2. Model Training Test

### Steps:
1. Click "Train Models Now" button in the alert
2. Confirm the dialog
3. **Expected**: Button shows spinner and "Training Models..."
4. **Expected**: Status badge shows "Training..."
5. Wait 10-30 seconds
6. **Expected**: Success toast appears
7. **Expected**: Status badge turns green with "Trained ✓"
8. **Expected**: Alert fades out after 2 seconds

### Verification:
```bash
# Check if models were saved
ls models/saved/
```

**Expected Files:**
- `best_model.pkl`
- `best_model_name.pkl`
- `vectorizer.pkl`

---

## 3. Scam Example Test

### Steps:
1. Click "Load Scam Example" button
2. **Expected**: Form pulses with animation
3. **Expected**: Success toast: "Scam example loaded!"
4. **Expected**: Form fields populated with scam data

### Verify Form Data:
- **Job Text**: Contains "CONGRATULATIONS", "Pay Rs 5000", "WhatsApp"
- **Company**: "Google India"
- **Email**: "hr.google.recruitment@gmail.com"
- **Contact Method**: "whatsapp"
- **Salary**: "2500"

### Analyze:
1. Click "Analyze for Fraud" button
2. **Expected**: Placeholder card disappears
3. **Expected**: Loading card appears with spinner
4. **Expected**: "Analyzing Job Posting..." message
5. Wait 2-5 seconds
6. **Expected**: Results card appears with animation
7. **Expected**: Success toast: "Analysis complete!"

### Verify Results:
- **Risk Score**: 75-95% (RED - CRITICAL or HIGH)
- **Risk Tier**: "CRITICAL FRAUD" or "HIGH SCAM LIKELIHOOD"
- **Recommendation**: "IGNORE" or "AVOID"
- **Component Scores**: All visible with progress bars
- **ML Detection**: Shows model name and probability
- **Fraud Patterns**: Multiple patterns matched
- **Risk Factors**: Several high-severity factors
- **Company Verification**: "Company Not Found" or low confidence
- **Salary Analysis**: Anomaly detected
- **Recruiter Trust**: Low trust score

### Download PDF:
1. Click "Download Forensic Report" button
2. **Expected**: PDF file downloads
3. Open PDF
4. **Expected**: Professional report with all analysis details

---

## 4. Legitimate Example Test

### Steps:
1. Click "Load Legitimate Example" button
2. **Expected**: Form pulses with animation
3. **Expected**: Success toast: "Legitimate example loaded!"
4. **Expected**: Form fields populated with legitimate data

### Verify Form Data:
- **Job Text**: Professional interview invitation
- **Company**: "Infosys Limited"
- **Email**: "recruitment@infosys.com"
- **Contact Method**: "email"
- **Salary**: "600"

### Analyze:
1. Click "Analyze for Fraud" button
2. Wait for results
3. **Expected**: Results card appears

### Verify Results:
- **Risk Score**: 10-30% (GREEN - LOW RISK)
- **Risk Tier**: "LOW RISK"
- **Recommendation**: "SAFE TO PROCEED"
- **Component Scores**: Mostly low values
- **ML Detection**: Low scam probability
- **Fraud Patterns**: Few or no patterns matched
- **Company Verification**: May find company (if API available)
- **Salary Analysis**: Within normal range
- **Recruiter Trust**: Higher trust score

---

## 5. Custom Input Test

### Test Case 1: Empty Form
1. Clear all fields
2. Click "Analyze for Fraud"
3. **Expected**: Error toast: "Please enter job description text"
4. **Expected**: Form not submitted

### Test Case 2: Short Text
1. Enter: "Job offer"
2. Click "Analyze for Fraud"
3. **Expected**: Error toast: "Job description is too short"
4. **Expected**: Form not submitted

### Test Case 3: Custom Scam Text
```
Urgent! Selected for Amazon. Salary 30 LPA. 
Pay Rs 3000 registration fee immediately. 
Contact via WhatsApp only.
```
1. Paste above text
2. Fill company: "Amazon"
3. Fill email: "hr@gmail.com"
4. Select contact: "whatsapp"
5. Enter salary: "3000"
6. Click "Analyze for Fraud"
7. **Expected**: High risk score (70-90%)

### Test Case 4: Custom Legitimate Text
```
We are pleased to invite you for an interview.
Date: Next Monday, 10 AM
Location: Our corporate office
Please bring your resume and certificates.
```
1. Paste above text
2. Fill company: "TCS"
3. Fill email: "careers@tcs.com"
4. Select contact: "email"
5. Enter salary: "800"
6. Click "Analyze for Fraud"
7. **Expected**: Low risk score (20-40%)

---

## 6. UI/UX Feature Tests

### Animation Tests:
1. **Hero Stats**: Hover over stat cards
   - **Expected**: Cards lift up with shadow
2. **Form Inputs**: Click on input fields
   - **Expected**: Blue border with glow effect
3. **Buttons**: Hover over buttons
   - **Expected**: Lift animation and shadow increase
4. **Results**: Scroll through results
   - **Expected**: Staggered fade-in animations

### Responsive Tests:
1. Resize browser to mobile width (< 768px)
   - **Expected**: Single column layout
   - **Expected**: Collapsible navigation menu
   - **Expected**: Smaller risk score font
2. Resize to tablet width (768px - 1024px)
   - **Expected**: Adjusted layouts
   - **Expected**: Readable text sizes

### Accessibility Tests:
1. Press Tab key repeatedly
   - **Expected**: Logical focus order
   - **Expected**: Visible focus indicators
2. Use screen reader (if available)
   - **Expected**: Proper labels announced
   - **Expected**: ARIA roles recognized

---

## 7. Error Handling Tests

### Test 1: Analyze Without Training
1. Delete `models/saved/` folder
2. Restart application
3. Try to analyze job posting
4. **Expected**: Analysis completes with default values
5. **Expected**: Risk score around 50%
6. **Expected**: No application crash

### Test 2: Network Error (Company Verification)
1. Disconnect internet
2. Analyze job posting with company name
3. **Expected**: Analysis completes
4. **Expected**: Company verification shows "unavailable"
5. **Expected**: Other components still work

### Test 3: Invalid Salary
1. Enter negative salary: "-100"
2. Analyze
3. **Expected**: Analysis handles gracefully
4. **Expected**: Salary analysis shows appropriate message

### Test 4: Special Characters
1. Enter job text with emojis and special characters
2. Analyze
3. **Expected**: Text preprocessor handles correctly
4. **Expected**: Analysis completes successfully

---

## 8. Performance Tests

### Load Time Test:
1. Open browser DevTools (F12)
2. Go to Network tab
3. Refresh page
4. **Expected**: Page loads in < 2 seconds
5. **Expected**: All assets load successfully

### Analysis Speed Test:
1. Start timer
2. Click "Analyze for Fraud"
3. Stop timer when results appear
4. **Expected**: Analysis completes in 2-5 seconds

### Multiple Analyses Test:
1. Analyze scam example
2. Immediately analyze legitimate example
3. Analyze custom text
4. **Expected**: All analyses complete successfully
5. **Expected**: No memory leaks or slowdowns

---

## 9. API Endpoint Tests

### Health Check:
```bash
curl http://localhost:5000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "ml_model_loaded": true,
  "model_name": "Decision Tree"
}
```

### Analyze Endpoint:
```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "job_text": "Pay Rs 5000 registration fee. Contact via WhatsApp.",
    "company_name": "Test Company",
    "recruiter_email": "test@gmail.com",
    "contact_method": "whatsapp",
    "offered_salary": 2000
  }'
```

**Expected**: JSON response with risk_score, risk_tier, etc.

### Train Endpoint:
```bash
curl -X POST http://localhost:5000/train
```

**Expected**: JSON response with training results

---

## 10. Browser Compatibility Tests

### Chrome/Edge (Chromium):
- ✅ All features work
- ✅ Animations smooth
- ✅ Gradients render correctly

### Firefox:
- ✅ All features work
- ✅ Backdrop blur supported
- ✅ Animations smooth

### Safari:
- ✅ Most features work
- ⚠️ Some CSS features may need prefixes
- ✅ Core functionality intact

### Mobile Browsers:
- ✅ Touch interactions work
- ✅ Responsive layout adapts
- ✅ Forms usable on mobile

---

## 11. Security Tests

### XSS Prevention:
1. Enter `<script>alert('XSS')</script>` in job text
2. Analyze
3. **Expected**: Script not executed
4. **Expected**: Text treated as plain text

### SQL Injection (N/A):
- No direct database queries
- All data processed in memory

### CSRF Protection:
- Consider adding CSRF tokens for production
- Current implementation: Development only

---

## 12. Regression Tests

After any code changes, verify:
- [ ] Application starts without errors
- [ ] Models can be trained
- [ ] Scam example detects high risk
- [ ] Legitimate example detects low risk
- [ ] PDF reports generate successfully
- [ ] All animations work
- [ ] Toast notifications appear
- [ ] Error handling works
- [ ] Responsive design intact

---

## 🐛 Known Issues & Workarounds

### Issue 1: Port Already in Use
**Error**: `Address already in use`
**Solution**: 
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Issue 2: NLTK Data Not Found
**Error**: `Resource stopwords not found`
**Solution**:
```bash
python -c "import nltk; nltk.download('all')"
```

### Issue 3: Models Not Loading
**Error**: `No saved models found`
**Solution**: Click "Train Models" button in UI

### Issue 4: PDF Generation Fails
**Error**: `PDF generation error`
**Solution**: Check `reports/` folder permissions

---

## ✅ Success Criteria

All tests pass if:
1. ✅ Application starts without errors
2. ✅ Models train successfully
3. ✅ Scam detection works (high risk for scams)
4. ✅ Legitimate detection works (low risk for legit)
5. ✅ UI is responsive and animated
6. ✅ Error handling prevents crashes
7. ✅ PDF reports generate
8. ✅ Toast notifications appear
9. ✅ All components render correctly
10. ✅ Performance is acceptable (< 5s analysis)

---

## 📊 Test Results Template

```
Test Date: ___________
Tester: ___________
Environment: Windows/Linux/Mac
Browser: Chrome/Firefox/Safari
Python Version: ___________

| Test Category | Status | Notes |
|--------------|--------|-------|
| Initial Setup | ✅/❌ | |
| Model Training | ✅/❌ | |
| Scam Detection | ✅/❌ | |
| Legit Detection | ✅/❌ | |
| UI/UX Features | ✅/❌ | |
| Error Handling | ✅/❌ | |
| Performance | ✅/❌ | |
| API Endpoints | ✅/❌ | |
| Browser Compat | ✅/❌ | |
| Security | ✅/❌ | |

Overall Result: PASS/FAIL
```

---

## 🎯 Quick Test (5 Minutes)

For rapid verification:
1. Start app: `python app.py`
2. Open: `http://localhost:5000`
3. Click "Train Models" → Wait → Success ✅
4. Click "Load Scam Example" → Analyze → High Risk ✅
5. Click "Load Legitimate Example" → Analyze → Low Risk ✅
6. Download PDF → Opens successfully ✅

**If all 6 steps pass, the application is working correctly!**

---

**Happy Testing! 🧪**
