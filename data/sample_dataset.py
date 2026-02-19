"""Enhanced training dataset for scam detection with 100+ samples"""

TRAINING_DATA = [
    # ===== SCAM EXAMPLES (label = 1) - 60 samples =====
    
    # Payment/Fee Scams
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
    ("Job confirmed! Pay Rs 2500 document verification charges. Salary 18 LPA. Start next week. Send payment to secure your position now.", 1),
    ("Congratulations! IBM hiring. 32 LPA package. Pay Rs 9000 background verification fee. Limited time offer. Contact via WhatsApp only.", 1),
    ("Earn 80000 monthly from home. Pay Rs 6000 training material fee. No experience required. Guaranteed income. Join immediately.", 1),
    ("Selected for Wipro. Salary 24 LPA. Pay Rs 5500 joining kit fee. Offer expires today. No interview needed. WhatsApp contact only.", 1),
    ("Urgent! Facebook job offer. 38 LPA for freshers. Pay Rs 12000 processing fee. Join within 24 hours. Contact on Telegram immediately.", 1),
    
    # Unrealistic Salary Scams
    ("Freshers welcome! Earn 50 LPA in your first year. No degree required. Simple data entry work. Apply now via WhatsApp.", 1),
    ("Amazing opportunity! 10th pass candidates can earn 35 LPA. Work from home. No interview. Just fill form and start earning.", 1),
    ("Guaranteed 60 LPA package for freshers. Top MNC hiring. No experience needed. Join today. Limited seats available.", 1),
    ("Earn 100000 per month working 2 hours daily. No skills required. Perfect for students and housewives. WhatsApp for details.", 1),
    ("Freshers get 45 LPA! Google, Amazon, Microsoft hiring. No interview process. Direct selection. Apply via WhatsApp now.", 1),
    ("Part-time job: Earn 75000 monthly. Work from anywhere. No qualifications needed. Guaranteed income. Contact immediately.", 1),
    ("12th pass? Earn 40 LPA! Top IT companies hiring. No experience required. Immediate joining. WhatsApp contact only.", 1),
    ("Earn 2 lakhs monthly from home. Simple copy-paste work. No investment except Rs 1000 registration. Guaranteed returns.", 1),
    ("Freshers salary 55 LPA! Apple, Tesla hiring in India. No interview. Direct offer letter. Pay Rs 5000 to confirm.", 1),
    ("Work 3 hours daily, earn 90000 monthly. No degree needed. Perfect for everyone. Join our team today via WhatsApp.", 1),
    
    # Urgency/Pressure Scams
    ("URGENT! Offer expires in 6 hours. Pay now or lose this opportunity. 30 LPA package. WhatsApp immediately.", 1),
    ("Last chance! Only 2 positions left. Pay Rs 4000 now. Salary 25 LPA. Offer closes tonight. Act fast!", 1),
    ("Hurry! Limited time offer. Pay registration fee within 2 hours. Miss this and regret forever. 35 LPA guaranteed.", 1),
    ("Final call! Offer expires at midnight. Pay Rs 6000 verification fee now. Don't miss this golden opportunity.", 1),
    ("Act now! Only 24 hours left. Pay processing fee immediately. 40 LPA package waiting. Last chance to apply.", 1),
    ("Urgent hiring! Positions filling fast. Pay Rs 3000 now to secure your spot. Offer valid for next 12 hours only.", 1),
    ("Time running out! Pay registration fee in next 3 hours. 28 LPA package. Don't let this opportunity slip away.", 1),
    ("Emergency hiring! Need immediate joiners. Pay Rs 5000 now. Salary 32 LPA. Offer expires in 8 hours.", 1),
    ("Last day to apply! Pay verification charges today. 38 LPA package. Tomorrow will be too late. Act now!", 1),
    ("Closing soon! Only few hours left. Pay Rs 7000 processing fee immediately. 42 LPA guaranteed. Hurry up!", 1),
    
    # WhatsApp/Telegram Only Contact Scams
    ("Selected for job! Contact only via WhatsApp +91-9876543210. No email, no calls. Salary 30 LPA. Pay Rs 5000 to confirm.", 1),
    ("Job offer from Google! Contact via Telegram only @jobscam123. Pay Rs 8000 registration. No other contact method available.", 1),
    ("Congratulations! You're hired. WhatsApp only communication. No office visit needed. Pay Rs 4000 to start. Salary 28 LPA.", 1),
    ("Selected for Amazon! Contact via WhatsApp immediately. Don't call or email. Pay Rs 6000 verification fee. 35 LPA package.", 1),
    ("Job confirmed! Telegram contact only. No phone calls accepted. Pay Rs 3500 processing fee. Salary 25 LPA guaranteed.", 1),
    ("Hired! WhatsApp is the only way to contact us. Pay Rs 5500 registration. No office address available. 32 LPA package.", 1),
    ("Selected! Contact via WhatsApp +91-XXXXXXXXXX only. No email communication. Pay Rs 7000 to confirm. 40 LPA salary.", 1),
    ("Job offer! Telegram only @scamjobs. No other contact method. Pay Rs 4500 verification. Salary 30 LPA. Join immediately.", 1),
    ("Congratulations! WhatsApp contact mandatory. No calls or emails. Pay Rs 6500 processing fee. 38 LPA package waiting.", 1),
    ("Hired by Microsoft! Contact via WhatsApp only. No office visit required. Pay Rs 8500 registration. 45 LPA guaranteed.", 1),
    
    # No Interview/Direct Selection Scams
    ("Selected without interview! Direct offer letter. Pay Rs 5000 to receive. Salary 30 LPA. No questions asked.", 1),
    ("Congratulations! You're hired without any interview. Just pay Rs 4000 registration. 28 LPA package. Start immediately.", 1),
    ("No interview needed! Direct selection based on your profile. Pay Rs 6000 verification fee. Salary 35 LPA guaranteed.", 1),
    ("Hired! No interview process. Pay Rs 3500 and get offer letter. 25 LPA package. Join next week without any formalities.", 1),
    ("Selected directly! No interview, no test. Just pay Rs 7000 processing fee. Salary 40 LPA. Immediate joining available.", 1),
    ("Congratulations! Direct hiring without interview. Pay Rs 5500 registration. 32 LPA package. No screening process required.", 1),
    ("You're hired! No interview necessary. Pay Rs 4500 verification. Salary 30 LPA. Direct offer letter will be sent.", 1),
    ("Selected! Skip all interviews. Pay Rs 8000 processing fee. 42 LPA package. Direct joining without any formalities.", 1),
    ("Hired without interview! Pay Rs 6500 registration. Salary 38 LPA. No questions, no tests. Just pay and join.", 1),
    ("Congratulations! Direct selection. No interview needed. Pay Rs 9000 verification. 45 LPA guaranteed. Start immediately.", 1),
    
    # Fake Company/Impersonation Scams
    ("Gooogle Inc hiring! Pay Rs 5000 registration. Salary 30 LPA. Contact via WhatsApp. Offer expires soon.", 1),
    ("Amazone India job offer! Pay Rs 6000 verification. 35 LPA package. No interview. WhatsApp contact only.", 1),
    ("Microsft Corporation hiring! Pay Rs 7000 processing fee. Salary 40 LPA. Urgent joining. Telegram contact.", 1),
    ("Infosys Technolgies job! Pay Rs 4000 registration. 28 LPA package. No interview needed. WhatsApp only.", 1),
    ("TCS Consultancy hiring! Pay Rs 5500 verification. Salary 32 LPA. Direct selection. Contact via WhatsApp.", 1),
    
    # ===== LEGITIMATE EXAMPLES (label = 0) - 60 samples =====
    
    # Professional Interview Invitations
    ("We are pleased to invite you for an interview at our Bangalore office. Please bring your resume and certificates. Interview scheduled for next Monday at 10 AM.", 0),
    ("Thank you for applying to Software Engineer position. We would like to schedule a technical interview. Please confirm your availability for next week.", 0),
    ("Your application has been shortlisted. Please attend the interview on 15th January at our corporate office. Bring original documents for verification.", 0),
    ("We are impressed with your profile and would like to invite you for an interview. Please visit our office next Tuesday at 2 PM.", 0),
    ("Congratulations on being shortlisted! We would like to schedule an interview with you. Please reply with your available dates and times.", 0),
    ("Your resume has been reviewed and we find you suitable for the position. Please attend interview on 20th March at our Mumbai office.", 0),
    ("We would like to invite you for a face-to-face interview. Please bring your updated resume and educational certificates. Date: 25th February.", 0),
    ("Thank you for your interest in our company. We would like to proceed with your application. Please attend interview next week.", 0),
    ("Your application for Senior Developer role has been shortlisted. Interview scheduled for 10th April at our Pune office at 11 AM.", 0),
    ("We are pleased to inform you that you have been selected for the next round of interviews. Please confirm your availability.", 0),
    
    # Proper Job Postings
    ("We are hiring for Software Engineer position. Salary range 12-18 LPA based on experience. Please apply through our careers portal with updated resume.", 0),
    ("Job opening for Senior Developer role. Experience: 5-7 years. Salary: 15-20 LPA. Please submit your application through our official website.", 0),
    ("We are looking for Marketing Manager. Required experience: 5+ years. CTC: 18-25 LPA. Apply via our company careers page.", 0),
    ("Hiring Full Stack Developer. Skills required: React, Node.js, MongoDB. Salary negotiable based on experience. Apply through LinkedIn or company portal.", 0),
    ("Position available: Business Analyst. Experience: 3-5 years. Salary: 10-15 LPA. Please send your resume to hr@company.com", 0),
    ("We are recruiting for Project Manager role. Experience: 8+ years. CTC: 20-30 LPA. Apply through our official careers website.", 0),
    ("Job vacancy: Data Scientist. Required skills: Python, ML, AI. Salary: 15-22 LPA. Submit application via company portal.", 0),
    ("Hiring for Product Manager position. Experience: 6-10 years. Salary range: 25-35 LPA. Apply through our careers page.", 0),
    ("Opening for Senior Consultant. Required experience: 10+ years. CTC: 30-40 LPA. Please apply via our official website.", 0),
    ("We are looking for DevOps Engineer. Experience: 4-6 years. Salary: 12-18 LPA. Apply through our company careers portal.", 0),
    
    # Campus Recruitment
    ("We are conducting campus recruitment drive. Eligible candidates can register through college placement cell. Multiple rounds of interviews will be conducted.", 0),
    ("Our company will be visiting your campus for recruitment. Interested students please register with placement office. No fees required.", 0),
    ("Campus hiring for fresher positions. Please register through your college placement cell. Interview process will be conducted on campus.", 0),
    ("We are coming to your college for recruitment drive. Freshers can apply through placement office. All rounds will be on campus.", 0),
    ("Campus placement drive scheduled for next month. Interested students register with placement cell. No registration fees required.", 0),
    ("Our company is conducting on-campus recruitment. Please contact your placement office for registration. Multiple positions available.", 0),
    ("Campus recruitment for fresher roles. Register through college placement cell. Interview and selection process on campus premises.", 0),
    ("We will be visiting your campus for hiring. Interested candidates register with placement office. No fees for registration or interview.", 0),
    ("On-campus recruitment drive announced. Students can register through placement cell. All interview rounds will be conducted on campus.", 0),
    ("Campus hiring program scheduled. Please register via college placement office. No charges for application or interview process.", 0),
    
    # Professional Communication
    ("Thank you for attending the first round. You have been selected for second round of interviews. HR will contact you with further details.", 0),
    ("We have reviewed your profile and would like to proceed with the next steps. Please check your email for interview schedule.", 0),
    ("Congratulations on clearing the technical round. Please attend HR round on 15th March at our office. Bring original documents.", 0),
    ("Your interview performance was impressive. We would like to extend an offer. Please visit our office for offer letter discussion.", 0),
    ("Thank you for your time in the interview. We will get back to you with our decision within one week. Please wait for our response.", 0),
    ("We are pleased to inform you that you have cleared all interview rounds. Please visit our office for offer letter and joining formalities.", 0),
    ("Your application is under review. We will contact you if your profile matches our requirements. Thank you for your interest.", 0),
    ("We have received your application. Our HR team will review it and contact you if you are shortlisted for interview.", 0),
    ("Thank you for applying. We are currently reviewing applications and will contact shortlisted candidates within two weeks.", 0),
    ("Your profile has been reviewed. We will schedule an interview if your qualifications match our requirements. Please wait for our response.", 0),
    
    # Detailed Job Descriptions
    ("Position: Software Engineer. Location: Bangalore. Experience: 2-4 years. Skills: Java, Spring Boot, MySQL. Salary: 10-15 LPA. Apply via careers page.", 0),
    ("Role: Senior Developer. Office: Mumbai. Experience: 5-7 years. Tech stack: React, Node.js, AWS. CTC: 18-25 LPA. Send resume to hr@company.com", 0),
    ("Hiring: Data Analyst. Location: Pune. Experience: 3-5 years. Skills: Python, SQL, Tableau. Salary: 12-18 LPA. Apply through company website.", 0),
    ("Opening: Product Manager. Office: Delhi. Experience: 6-8 years. Domain: E-commerce. CTC: 25-35 LPA. Submit application via careers portal.", 0),
    ("Vacancy: DevOps Engineer. Location: Hyderabad. Experience: 4-6 years. Skills: Docker, Kubernetes, Jenkins. Salary: 15-20 LPA. Apply online.", 0),
    ("Position: Business Analyst. Office: Chennai. Experience: 3-5 years. Domain: Finance. CTC: 12-18 LPA. Send resume to recruitment@company.com", 0),
    ("Role: QA Engineer. Location: Bangalore. Experience: 2-4 years. Skills: Selenium, API testing. Salary: 8-12 LPA. Apply via company portal.", 0),
    ("Hiring: UI/UX Designer. Office: Mumbai. Experience: 3-5 years. Tools: Figma, Adobe XD. CTC: 10-15 LPA. Submit portfolio and resume.", 0),
    ("Opening: Cloud Architect. Location: Pune. Experience: 8-10 years. Skills: AWS, Azure, GCP. Salary: 30-40 LPA. Apply through careers page.", 0),
    ("Vacancy: Scrum Master. Office: Bangalore. Experience: 5-7 years. Certification: CSM required. CTC: 18-25 LPA. Send resume to hr@company.com", 0),
    
    # Internship Opportunities
    ("Summer internship program for engineering students. Duration: 2 months. Stipend: Rs 15000/month. Apply through our careers portal.", 0),
    ("We are offering internship opportunities for final year students. Duration: 6 months. Stipend provided. Apply via company website.", 0),
    ("Internship program for MBA students. Duration: 3 months. Stipend: Rs 20000/month. Submit application through careers page.", 0),
    ("Looking for interns in software development. Duration: 4 months. Stipend: Rs 18000/month. Apply through our official portal.", 0),
    ("Internship opportunity in data science. Duration: 6 months. Stipend provided. For final year students. Apply via company website.", 0),
    ("We are hiring interns for marketing team. Duration: 3 months. Stipend: Rs 12000/month. Submit application online.", 0),
    ("Internship program in product management. Duration: 5 months. Stipend provided. For MBA students. Apply through careers portal.", 0),
    ("Looking for design interns. Duration: 4 months. Stipend: Rs 15000/month. Portfolio required. Apply via company website.", 0),
    ("Internship in business analytics. Duration: 6 months. Stipend: Rs 20000/month. For engineering/MBA students. Apply online.", 0),
    ("We are offering internships in HR department. Duration: 3 months. Stipend provided. For MBA students. Submit application via portal.", 0),
    
    # Follow-up Communications
    ("Thank you for your patience. We are still reviewing applications and will contact you soon with an update on your application status.", 0),
    ("We appreciate your interest in our company. Your application is under consideration. We will notify you of the next steps shortly.", 0),
    ("Thank you for attending the interview. We are currently evaluating all candidates and will inform you of our decision within a week.", 0),
    ("We have received your application for the position. Our team is reviewing it and will contact you if you are selected for interview.", 0),
    ("Thank you for your time during the interview process. We will complete our evaluation and get back to you with feedback soon.", 0),
    ("Your application has been received and is being reviewed by our hiring team. We will contact you if your profile matches our requirements.", 0),
    ("We appreciate your interest in joining our team. Your application is under review and we will update you on the status shortly.", 0),
    ("Thank you for applying to our company. We are currently screening applications and will contact shortlisted candidates for interviews.", 0),
    ("We have received your resume and it is being reviewed by our recruitment team. We will reach out if you are selected for next round.", 0),
    ("Thank you for your application. We are in the process of reviewing all candidates and will notify you of any updates soon.", 0),
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
        "Your application has been shortlisted. Please attend interview on Monday.",
        "Selected for Google! 50 LPA for freshers. Pay Rs 10000 verification fee. WhatsApp only.",
        "We are conducting campus recruitment. Register through placement cell. No fees required."
    ]

def get_dataset_stats():
    """Return dataset statistics"""
    scam_count = sum(1 for item in TRAINING_DATA if item[1] == 1)
    legit_count = sum(1 for item in TRAINING_DATA if item[1] == 0)
    return {
        'total_samples': len(TRAINING_DATA),
        'scam_samples': scam_count,
        'legitimate_samples': legit_count,
        'balance_ratio': f"{scam_count}:{legit_count}"
    }
