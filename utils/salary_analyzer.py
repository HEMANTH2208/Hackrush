import re
import numpy as np

class SalaryAnalyzer:
    """Detect unrealistic salary offers"""
    
    def __init__(self):
        # Market salary ranges by job level (in thousands per year)
        self.salary_benchmarks = {
            'entry': {'min': 300, 'max': 600, 'median': 400},
            'junior': {'min': 400, 'max': 800, 'median': 600},
            'mid': {'min': 600, 'max': 1500, 'median': 1000},
            'senior': {'min': 1200, 'max': 3000, 'median': 2000},
            'lead': {'min': 2000, 'max': 5000, 'median': 3000}
        }
    
    def extract_salary(self, text):
        """Extract salary information from text"""
        # Patterns for salary extraction
        patterns = [
            r'(\d+)\s*(?:k|thousand)\s*(?:to|-)?\s*(\d+)?\s*(?:k|thousand)?',
            r'(?:rs|inr|₹)\s*(\d+(?:,\d+)*)',
            r'(\d+)\s*(?:lpa|lakh)',
            r'salary\s*(?:of|:)?\s*(?:rs|inr|₹)?\s*(\d+(?:,\d+)*)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                try:
                    salary = int(re.sub(r'[^\d]', '', match.group(1)))
                    return salary
                except:
                    continue
        
        return None
    
    def detect_job_level(self, text):
        """Detect job level from text"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['entry', 'fresher', 'graduate', 'trainee']):
            return 'entry'
        elif any(word in text_lower for word in ['junior', 'associate']):
            return 'junior'
        elif any(word in text_lower for word in ['senior', 'sr']):
            return 'senior'
        elif any(word in text_lower for word in ['lead', 'principal', 'architect']):
            return 'lead'
        else:
            return 'mid'
    
    def analyze_salary(self, text, offered_salary=None):
        """Analyze salary for anomalies"""
        if offered_salary is None:
            offered_salary = self.extract_salary(text)
        
        if offered_salary is None:
            return {
                'anomaly_detected': False,
                'anomaly_score': 0,
                'message': 'No salary information found'
            }
        
        job_level = self.detect_job_level(text)
        benchmark = self.salary_benchmarks[job_level]
        
        # Calculate z-score
        median = benchmark['median']
        std_dev = (benchmark['max'] - benchmark['min']) / 4
        z_score = abs((offered_salary - median) / std_dev)
        
        # Determine anomaly
        anomaly_score = 0
        anomaly_detected = False
        message = ""
        
        if offered_salary > benchmark['max'] * 1.5:
            anomaly_detected = True
            anomaly_score = min(100, int(z_score * 20))
            message = f"Salary significantly above market rate for {job_level} level"
        elif offered_salary < benchmark['min'] * 0.5:
            anomaly_detected = True
            anomaly_score = min(100, int(z_score * 15))
            message = f"Salary significantly below market rate for {job_level} level"
        elif offered_salary > benchmark['max']:
            anomaly_score = min(50, int(z_score * 10))
            message = f"Salary above typical range for {job_level} level"
        
        return {
            'anomaly_detected': anomaly_detected,
            'anomaly_score': anomaly_score,
            'offered_salary': offered_salary,
            'job_level': job_level,
            'benchmark_range': f"{benchmark['min']}-{benchmark['max']}k",
            'z_score': round(z_score, 2),
            'message': message
        }
