"""Sample training dataset for scam detection"""

TRAINING_DATA = [
    # Scam examples (label = 1)
    ("Congratulations! You are selected for the position. Pay Rs 5000 registration fee to confirm your joining. Contact via WhatsApp only.", 1),
    ("Urgent hiring! Earn 50000 per month working from home. No experience needed. Send processing fee of Rs 3000 to get started immediately.", 1),
    ("You have been shortlisted for Google. Salary 25 LPA. Join within 24 hours. Pay interview fee Rs 2000. Contact on WhatsApp +91-XXXXXXXXXX", 1),
    ("Immediate job offer! Work from home and earn lakhs. No interview required. Just pay Rs 1500 registration and start earning today!", 1),
    ("Congratulations! Selected for Amazon. Salary 30 LPA for freshers. Pay Rs 4000 deposit. Offer expires in 24 hours. WhatsApp only.", 1),
    ("Guaranteed job placement. Pay Rs 10000 training fee. Get job in top MNC with 20 LPA package. No experience needed. Contact immediately.", 1),
    ("You won job lottery! Selected without interview. Salary 40 LPA. Send Rs 5000 to this wallet address to confirm. Urgent joining required.", 1),
    ("Part time job offer. Earn 3000 daily from home. Just pay Rs 500 registration. No skills required. Easy money guaranteed. WhatsApp now.", 1),
    ("Congratulations! Microsoft job offer. 35 LPA package. Pay processing fee Rs 8000. Join tomorrow. Contact via Telegram only.", 1),
    ("Urgent requirement! Data entry job. Earn 50000 monthly. Pay Rs 2000 registration fee. No interview. Immediate joining. WhatsApp contact.", 1),
    ("Selected for Apple Inc. Salary 45 LPA. Pay Rs 6000 verification fee. Offer valid for 12 hours only. Contact on WhatsApp immediately.", 1),
    ("Work from home opportunity! Earn lakhs monthly. Just invest Rs 5000. Guaranteed returns. No experience needed. Join today via WhatsApp.", 1),
    ("Congratulations! You are hired. Salary 28 LPA. Send Rs 3500 to secure position. Joining within 48 hours mandatory. WhatsApp only.", 1),
    ("Immediate job opening! Earn 60000 per month. Pay Rs 4500 training fee. No interview required. Easy work from home. Contact now.", 1),
    ("Selected for TCS. Package 22 LPA for freshers. Pay Rs 7000 onboarding fee. Urgent joining. No interview. WhatsApp for details.", 1),
    
    # Legitimate examples (label = 0)
    ("We are pleased to invite you for an interview at our Bangalore office. Please bring your resume and certificates. Interview scheduled for next Monday at 10 AM.", 0),
    ("Thank you for applying to Software Engineer position. We would like to schedule a technical interview. Please confirm your availability for next week.", 0),
    ("Your application has been shortlisted. Please attend the interview on 15th January at our corporate office. Bring original documents for verification.", 0),
    ("We are hiring for Senior Developer role. Salary range 12-18 LPA based on experience. Please apply through our careers portal with updated resume.", 0),
    ("Interview invitation for Data Analyst position. First round will be telephonic screening followed by technical and HR rounds. No fees required.", 0),
    ("Thank you for your interest in our company. We have reviewed your profile and would like to proceed with the interview process. Please check your email for details.", 0),
    ("Job opening for Marketing Manager. Experience: 5-7 years. Salary: 15-20 LPA. Please submit your application through our official website.", 0),
    ("We are conducting campus recruitment drive. Eligible candidates can register through college placement cell. Multiple rounds of interviews will be conducted.", 0),
    ("Your resume has been reviewed for the Product Manager role. We would like to schedule a video interview. Please share your convenient time slots.", 0),
    ("Hiring for Full Stack Developer. Required skills: React, Node.js, MongoDB. Salary negotiable based on experience. Apply via LinkedIn or company portal.", 0),
    ("Interview scheduled for Business Analyst position on 20th March. Venue: Corporate office, Mumbai. Please arrive 15 minutes early with documents.", 0),
    ("We have an opening for Senior Consultant. CTC: 18-25 LPA. Candidates with 8+ years experience may apply. Send resume to hr@company.com", 0),
    ("Thank you for attending the first round. You have been selected for second round of interviews. HR will contact you with further details.", 0),
    ("Job opportunity in our Delhi office. Role: Project Manager. Experience: 10+ years. Competitive salary package. Apply through our careers page.", 0),
    ("We are impressed with your profile. Please attend final round of interview with our CTO. Date and time will be communicated via email.", 0),
]

def get_training_data():
    """Return training texts and labels"""
    texts = [item[0] for item in TRAINING_DATA]
    labels = [item[1] for item in TRAINING_DATA]
    return texts, labels

def get_test_samples():
    """Return sample test cases"""
    return [
        "Congratulations! Pay Rs 2000 registration fee. Join immediately via WhatsApp.",
        "We would like to invite you for an interview at our office next week.",
        "Earn 100000 monthly from home. No experience needed. Pay Rs 5000 to start.",
        "Your application has been shortlisted. Please attend interview on Monday."
    ]
