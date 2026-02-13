from flask import Flask, render_template, request, jsonify, send_file
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

# Import utility modules
from utils.text_preprocessor import TextPreprocessor
from utils.fraud_rules import FraudRuleEngine
from utils.salary_analyzer import SalaryAnalyzer
from utils.company_verifier import CompanyVerifier
from utils.mca_verifier import MCAVerifier
from utils.recruiter_scorer import RecruiterScorer
from utils.risk_fusion import RiskFusionEngine
from utils.pdf_generator import ForensicReportGenerator

# Import ML classifier
from models.ml_classifier import MLScamClassifier

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize components
preprocessor = TextPreprocessor()
rule_engine = FraudRuleEngine()
salary_analyzer = SalaryAnalyzer()
company_verifier = CompanyVerifier(api_key=os.getenv('OPENCORPORATES_API_KEY'))
mca_verifier = MCAVerifier()
recruiter_scorer = RecruiterScorer()
risk_fusion = RiskFusionEngine()
pdf_generator = ForensicReportGenerator()
ml_classifier = MLScamClassifier()

# Try to load pre-trained models
ml_classifier.load_models()

def extract_text_from_url(url):
    """Extract job posting text from URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text[:5000]  # Limit to first 5000 characters
    except Exception as e:
        raise Exception(f"Failed to extract text from URL: {str(e)}")

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_job():
    """Analyze job posting for fraud"""
    try:
        # Get input data
        data = request.json
        input_type = data.get('input_type', 'text')  # text, link, whatsapp
        job_text = ''
        
        # Handle different input types
        if input_type == 'link':
            job_link = data.get('job_link', '')
            if not job_link:
                return jsonify({'error': 'Job link is required'}), 400
            try:
                job_text = extract_text_from_url(job_link)
            except Exception as e:
                return jsonify({'error': str(e)}), 400
        elif input_type == 'whatsapp':
            job_text = data.get('whatsapp_text', '')
            whatsapp_number = data.get('whatsapp_number', '')
            # Add WhatsApp context to analysis
            if whatsapp_number:
                job_text = f"WhatsApp Number: {whatsapp_number}\n\n{job_text}"
        else:  # text
            job_text = data.get('job_text', '')
        
        company_name = data.get('company_name', '')
        recruiter_email = data.get('recruiter_email', '')
        contact_method = data.get('contact_method', '')
        linkedin_url = data.get('linkedin_url', '')
        offered_salary = data.get('offered_salary')
        
        if not job_text:
            return jsonify({'error': 'Job text is required'}), 400
        
        if len(job_text) < 20:
            return jsonify({'error': 'Job text is too short. Please provide more details.'}), 400
        
        # 1. Preprocess text
        try:
            preprocessed_text = preprocessor.preprocess(job_text)
            text_features = preprocessor.extract_features(job_text)
        except Exception as e:
            print(f"Preprocessing error: {e}")
            preprocessed_text = job_text.lower()
            text_features = {}
        
        # 2. ML Classification
        try:
            ml_result = ml_classifier.predict(preprocessed_text)
        except Exception as e:
            print(f"ML classification error: {e}")
            ml_result = {
                'is_scam': False,
                'probability': 50.0,
                'confidence': 'low',
                'model': 'default'
            }
        
        # 3. Rule-based detection
        try:
            rule_result = rule_engine.check_rules(job_text)
            evidence = rule_engine.get_evidence(job_text, rule_result['triggered_rules'])
        except Exception as e:
            print(f"Rule engine error: {e}")
            rule_result = {'triggered_rules': [], 'rule_score': 0, 'high_confidence_scam': False}
            evidence = []
        
        # 4. Company verification (both OpenCorporates and MCA)
        company_result = {'found': False, 'confidence': 50}
        mca_result = {'found': False, 'confidence': 0}
        
        if company_name:
            try:
                # Try OpenCorporates first
                company_result = company_verifier.verify_company(company_name)
                
                # Also try MCA for Indian companies
                mca_result = mca_verifier.verify_indian_company(company_name)
                
                # Combine results - use higher confidence
                if mca_result['confidence'] > company_result.get('confidence', 0):
                    company_result = mca_result
                    company_result['verification_source'] = 'MCA (India)'
                else:
                    company_result['verification_source'] = 'OpenCorporates'
                
                if recruiter_email:
                    email_match = company_verifier.verify_email_domain(recruiter_email, company_name)
                    company_result['email_match'] = email_match
            except Exception as e:
                print(f"Company verification error: {e}")
                company_result = {'found': False, 'confidence': 50, 'message': 'Verification unavailable'}
        
        # 5. Salary analysis
        try:
            salary_result = salary_analyzer.analyze_salary(job_text, offered_salary)
        except Exception as e:
            print(f"Salary analysis error: {e}")
            salary_result = {'anomaly_detected': False, 'anomaly_score': 0, 'message': 'Analysis unavailable'}
        
        # 6. Recruiter scoring
        try:
            recruiter_result = recruiter_scorer.score_recruiter(
                email=recruiter_email,
                contact_method=contact_method,
                linkedin_url=linkedin_url
            )
        except Exception as e:
            print(f"Recruiter scoring error: {e}")
            recruiter_result = {'trust_score': 50, 'trust_level': 'MODERATE_TRUST', 'factors': []}
        
        # 7. Risk fusion
        try:
            risk_signals = {
                'ml_probability': ml_result['probability'],
                'rule_score': rule_result['rule_score'],
                'company_confidence': company_result.get('confidence', 50),
                'salary_anomaly_score': salary_result.get('anomaly_score', 0),
                'recruiter_trust_score': recruiter_result['trust_score']
            }
            
            risk_result = risk_fusion.calculate_risk_score(risk_signals)
            explanations = risk_fusion.get_explanation(risk_signals, risk_result)
        except Exception as e:
            print(f"Risk fusion error: {e}")
            risk_result = {
                'risk_score': 50.0,
                'risk_tier': 'MODERATE_RISK',
                'recommendation': 'Unable to complete full analysis',
                'component_scores': {}
            }
            explanations = []
        
        # Compile final result
        analysis_result = {
            'input_type': input_type,
            'risk_score': risk_result['risk_score'],
            'risk_tier': risk_result['risk_tier'],
            'recommendation': risk_result['recommendation'],
            'component_scores': risk_result['component_scores'],
            'ml_result': ml_result,
            'rule_result': rule_result,
            'triggered_rules': rule_result['triggered_rules'],
            'company_verification': company_result,
            'mca_verification': mca_result if company_name else None,
            'salary_analysis': salary_result,
            'recruiter_score': recruiter_result,
            'explanations': explanations,
            'evidence': evidence
        }
        
        # 8. Generate PDF report
        try:
            pdf_path = pdf_generator.generate_report(analysis_result, job_text)
            analysis_result['pdf_report'] = os.path.basename(pdf_path)
        except Exception as e:
            print(f"PDF generation error: {e}")
            analysis_result['pdf_report'] = 'report_unavailable.pdf'
        
        return jsonify(analysis_result)
    
    except Exception as e:
        print(f"General error in analyze_job: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_report(filename):
    """Download PDF report"""
    try:
        filepath = os.path.join('reports', filename)
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/train', methods=['POST'])
def train_models():
    """Train ML models with sample data"""
    try:
        from data.sample_dataset import get_training_data
        
        texts, labels = get_training_data()
        results = ml_classifier.train_models(texts, labels)
        
        return jsonify({
            'message': 'Models trained successfully',
            'best_model': ml_classifier.best_model_name,
            'results': {name: {'cv_f1': res['cv_f1_mean']} for name, res in results.items()}
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'ml_model_loaded': ml_classifier.best_model is not None,
        'model_name': ml_classifier.best_model_name
    })

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('reports', exist_ok=True)
    os.makedirs('models/saved', exist_ok=True)
    
    print("=" * 50)
    print("JobShield AI - Recruitment Scam Detection System")
    print("=" * 50)
    print("\nStarting server...")
    print("Access dashboard at: http://localhost:5000")
    print("\nNote: Train models first by clicking 'Train Models' button")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
