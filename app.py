from flask import Flask, render_template, request, jsonify, send_file
import os
from dotenv import load_dotenv

# Import utility modules
from utils.text_preprocessor import TextPreprocessor
from utils.fraud_rules import FraudRuleEngine
from utils.salary_analyzer import SalaryAnalyzer
from utils.company_verifier import CompanyVerifier
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
recruiter_scorer = RecruiterScorer()
risk_fusion = RiskFusionEngine()
pdf_generator = ForensicReportGenerator()
ml_classifier = MLScamClassifier()

# Try to load pre-trained models
ml_classifier.load_models()

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
        job_text = data.get('job_text', '')
        company_name = data.get('company_name', '')
        recruiter_email = data.get('recruiter_email', '')
        contact_method = data.get('contact_method', '')
        linkedin_url = data.get('linkedin_url', '')
        offered_salary = data.get('offered_salary')
        
        if not job_text:
            return jsonify({'error': 'Job text is required'}), 400
        
        # 1. Preprocess text
        preprocessed_text = preprocessor.preprocess(job_text)
        text_features = preprocessor.extract_features(job_text)
        
        # 2. ML Classification
        ml_result = ml_classifier.predict(preprocessed_text)
        
        # 3. Rule-based detection
        rule_result = rule_engine.check_rules(job_text)
        evidence = rule_engine.get_evidence(job_text, rule_result['triggered_rules'])
        
        # 4. Company verification
        company_result = {'found': False, 'confidence': 50}
        if company_name:
            company_result = company_verifier.verify_company(company_name)
            if recruiter_email:
                email_match = company_verifier.verify_email_domain(recruiter_email, company_name)
                company_result['email_match'] = email_match
        
        # 5. Salary analysis
        salary_result = salary_analyzer.analyze_salary(job_text, offered_salary)
        
        # 6. Recruiter scoring
        recruiter_result = recruiter_scorer.score_recruiter(
            email=recruiter_email,
            contact_method=contact_method,
            linkedin_url=linkedin_url
        )
        
        # 7. Risk fusion
        risk_signals = {
            'ml_probability': ml_result['probability'],
            'rule_score': rule_result['rule_score'],
            'company_confidence': company_result.get('confidence', 50),
            'salary_anomaly_score': salary_result.get('anomaly_score', 0),
            'recruiter_trust_score': recruiter_result['trust_score']
        }
        
        risk_result = risk_fusion.calculate_risk_score(risk_signals)
        explanations = risk_fusion.get_explanation(risk_signals, risk_result)
        
        # Compile final result
        analysis_result = {
            'risk_score': risk_result['risk_score'],
            'risk_tier': risk_result['risk_tier'],
            'recommendation': risk_result['recommendation'],
            'component_scores': risk_result['component_scores'],
            'ml_result': ml_result,
            'rule_result': rule_result,
            'triggered_rules': rule_result['triggered_rules'],
            'company_verification': company_result,
            'salary_analysis': salary_result,
            'recruiter_score': recruiter_result,
            'explanations': explanations,
            'evidence': evidence
        }
        
        # 8. Generate PDF report
        pdf_path = pdf_generator.generate_report(analysis_result, job_text)
        analysis_result['pdf_report'] = os.path.basename(pdf_path)
        
        return jsonify(analysis_result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
