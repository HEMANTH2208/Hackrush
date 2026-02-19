# Quick Test Guide - Brutalist Theme

## Start the Application

```bash
python app.py
```

Open browser: http://localhost:5000

## Test Sequence

### 1. First Time Setup (30 seconds)
1. Click **"TRAIN MODELS"** button in the alert
2. Wait for success message
3. Alert should disappear
4. Status should show "READY ✓"

### 2. Test TEXT Input (Scam Example)
1. Click **"TRY SCAM EXAMPLE"** button
2. Review the loaded text (fake Google job with payment request)
3. Click **"ANALYZE FOR FRAUD"**
4. Wait 2-5 seconds
5. **Expected Results:**
   - Risk Score: 80-95% (RED)
   - Risk Tier: HIGH SCAM LIKELIHOOD or CRITICAL FRAUD PATTERN
   - Multiple fraud patterns detected
   - Company verification may fail (fake company)
   - High salary anomaly
   - Low recruiter trust

### 3. Test TEXT Input (Legitimate Example)
1. Click **"TRY LEGITIMATE EXAMPLE"** button
2. Review the loaded text (Infosys interview invitation)
3. Click **"ANALYZE FOR FRAUD"**
4. **Expected Results:**
   - Risk Score: 10-30% (GREEN)
   - Risk Tier: LOW RISK
   - Few or no fraud patterns
   - Company found (Infosys Limited)
   - Normal salary range
   - Higher recruiter trust

### 4. Test LINK Input
1. Click **"LINK"** tab
2. Enter a job posting URL (e.g., from Naukri, LinkedIn, Indeed)
   - Example: `https://www.naukri.com/job-listings-software-engineer-jobs`
3. Click **"ANALYZE LINK"**
4. **Expected Results:**
   - Text extracted from URL
   - Analysis performed
   - Results displayed

**Note:** Some sites may block scraping. If error occurs, try a different URL.

### 5. Test WHATSAPP Input
1. Click **"WHATSAPP"** tab
2. Paste this test message:
```
🎉 CONGRATULATIONS! You are SELECTED for Amazon India!

Position: Software Developer
Salary: 30 LPA for FRESHERS!

⚠️ URGENT: Pay Rs 10,000 registration fee within 24 HOURS!

Contact ONLY via WhatsApp: +91-9876543210

Limited seats! Don't miss this opportunity!
```
3. Optionally add WhatsApp number: `+91-9876543210`
4. Click **"ANALYZE WHATSAPP MESSAGE"**
5. **Expected Results:**
   - High risk score (85-95%)
   - Payment request detected
   - Urgency pattern detected
   - WhatsApp-only contact flagged
   - Unrealistic salary for freshers

### 6. Test MCA Verification
1. Go back to **"TEXT"** tab
2. Click **"SHOW ADVANCED OPTIONS"**
3. Enter Company Name: `Infosys Limited`
4. Enter any job text (or use sample)
5. Click **"ANALYZE FOR FRAUD"**
6. Scroll to **"COMPANY VERIFICATION"** section
7. **Expected Results:**
   - Company Found in Registry ✓
   - Confidence: 90%
   - Verification Source: MCA (INDIA)
   - Indicators: PRIVATE LIMITED COMPANY, INDIA-BASED, IT/SERVICES COMPANY

### 7. Test Company Not Found
1. In Advanced Options, enter Company Name: `Fake Company XYZ 123`
2. Click **"ANALYZE FOR FRAUD"**
3. **Expected Results:**
   - Company Not Found ✗
   - Low confidence
   - Warning message displayed

### 8. Test PDF Report Download
1. After any analysis, click **"DOWNLOAD FORENSIC REPORT"**
2. PDF should download
3. Open PDF to verify contents

## Visual Checks

### Brutalist Theme Elements
- [ ] Neon green (#39FF14) accents throughout
- [ ] Deep charcoal (#1C1C1C) backgrounds
- [ ] Monospace font (Courier New)
- [ ] UPPERCASE text on labels and buttons
- [ ] Sharp corners (no border-radius)
- [ ] Heavy borders (3px-5px)
- [ ] Box shadows on cards
- [ ] Color-coded risk scores (red/orange/green)

### UI Components
- [ ] Navigation bar with neon green border
- [ ] Hero section with large UPPERCASE heading
- [ ] Three input tabs (TEXT, LINK, WHATSAPP)
- [ ] Form controls with neon green borders
- [ ] Buttons with box shadows
- [ ] Progress bars with color coding
- [ ] Toast notifications (success/error)
- [ ] Loading spinner during analysis
- [ ] Results card with all sections

### Responsive Design
- [ ] Test on mobile (< 768px)
- [ ] Test on tablet (768px - 1024px)
- [ ] Test on desktop (> 1024px)

## Common Issues & Solutions

### Issue: Models not trained
**Solution:** Click "TRAIN MODELS" button and wait 30 seconds

### Issue: "Analysis failed" error
**Solution:** 
1. Check if models are trained
2. Ensure text is at least 20 characters
3. Check console for errors

### Issue: Link scraping fails
**Solution:**
1. Try a different URL
2. Some sites block scraping
3. Use TEXT input instead

### Issue: Company not found
**Solution:**
1. Check spelling
2. Try full company name (e.g., "Infosys Limited" not "Infosys")
3. MCA only recognizes major Indian companies

### Issue: PDF download fails
**Solution:**
1. Check if `reports/` folder exists
2. Ensure write permissions
3. Check console for errors

## Performance Benchmarks

- **Model Training:** 10-30 seconds (one-time)
- **Text Analysis:** 2-5 seconds
- **Link Scraping:** 3-10 seconds (depends on site)
- **PDF Generation:** 1-2 seconds

## Browser Console

Open Developer Tools (F12) to check for:
- JavaScript errors
- Network requests
- API responses
- Console logs

## Success Criteria

✅ All three input types work
✅ MCA verification displays correctly
✅ Risk scores calculate properly
✅ Results display in brutalist theme
✅ All text is UPPERCASE where appropriate
✅ PDF reports generate and download
✅ Toast notifications appear
✅ No console errors
✅ Responsive on all screen sizes

## Quick Demo Script (2 minutes)

1. **Start:** "This is JobShield AI with brutalist neon green theme"
2. **Train:** Click "TRAIN MODELS" (show loading)
3. **Scam Test:** Click "TRY SCAM EXAMPLE" → Analyze → Show 90% risk score
4. **Legit Test:** Click "TRY LEGITIMATE EXAMPLE" → Analyze → Show 15% risk score
5. **MCA:** Show Infosys verification with MCA badge
6. **Tabs:** Quickly show LINK and WHATSAPP tabs
7. **PDF:** Download a report
8. **Finish:** "Three input types, MCA verification, brutalist design - complete!"

---

**Total Test Time:** 10-15 minutes
**Demo Time:** 2-3 minutes
**Status:** Ready for presentation ✅
