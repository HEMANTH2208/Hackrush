class RiskFusionEngine:
    """Fuse multiple risk signals into unified fraud score"""
    
    def __init__(self):
        # Weights for different risk components
        self.weights = {
            'ml_probability': 0.35,
            'rule_score': 0.25,
            'company_verification': 0.20,
            'salary_anomaly': 0.10,
            'recruiter_trust': 0.10
        }
    
    def calculate_risk_score(self, signals):
        """Calculate unified risk score from multiple signals"""
        # Extract signals with defaults
        ml_prob = signals.get('ml_probability', 50)
        rule_score = signals.get('rule_score', 0)
        company_conf = signals.get('company_confidence', 50)
        salary_anomaly = signals.get('salary_anomaly_score', 0)
        recruiter_trust = signals.get('recruiter_trust_score', 50)
        
        # Invert company confidence (high confidence = low risk)
        company_risk = 100 - company_conf
        
        # Invert recruiter trust (high trust = low risk)
        recruiter_risk = 100 - recruiter_trust
        
        # Calculate weighted risk score
        risk_score = (
            ml_prob * self.weights['ml_probability'] +
            rule_score * self.weights['rule_score'] +
            company_risk * self.weights['company_verification'] +
            salary_anomaly * self.weights['salary_anomaly'] +
            recruiter_risk * self.weights['recruiter_trust']
        )
        
        # Normalize to 0-100
        risk_score = max(0, min(100, risk_score))
        
        # Determine risk tier
        risk_tier = self._classify_risk_tier(risk_score)
        
        # Generate recommendation
        recommendation = self._generate_recommendation(risk_score, risk_tier)
        
        return {
            'risk_score': round(risk_score, 2),
            'risk_tier': risk_tier,
            'recommendation': recommendation,
            'component_scores': {
                'ml_probability': ml_prob,
                'rule_score': rule_score,
                'company_risk': company_risk,
                'salary_anomaly': salary_anomaly,
                'recruiter_risk': recruiter_risk
            }
        }
    
    def _classify_risk_tier(self, score):
        """Classify risk into tiers"""
        if score >= 75:
            return 'CRITICAL_FRAUD'
        elif score >= 50:
            return 'HIGH_SCAM_LIKELIHOOD'
        elif score >= 30:
            return 'MODERATE_RISK'
        else:
            return 'LOW_RISK'
    
    def _generate_recommendation(self, score, tier):
        """Generate user recommendation based on risk"""
        recommendations = {
            'CRITICAL_FRAUD': 'IGNORE - Report immediately to authorities. Do not engage.',
            'HIGH_SCAM_LIKELIHOOD': 'AVOID - Strong indicators of fraud. Do not proceed.',
            'MODERATE_RISK': 'PROCEED WITH CAUTION - Verify company and recruiter independently.',
            'LOW_RISK': 'SAFE TO PROCEED - Standard verification recommended.'
        }
        return recommendations.get(tier, 'Unknown risk level')
    
    def get_explanation(self, signals, risk_result):
        """Generate explainable evidence for the risk score"""
        explanations = []
        
        # ML model explanation
        if signals.get('ml_probability', 0) > 60:
            explanations.append({
                'factor': 'ML Model Detection',
                'severity': 'high',
                'detail': f"AI model detected {signals['ml_probability']:.1f}% fraud probability"
            })
        
        # Rule engine explanation
        if signals.get('rule_score', 0) > 40:
            explanations.append({
                'factor': 'Fraud Pattern Match',
                'severity': 'high',
                'detail': f"Matched known scam patterns (score: {signals['rule_score']})"
            })
        
        # Company verification
        if signals.get('company_confidence', 100) < 50:
            explanations.append({
                'factor': 'Company Verification Failed',
                'severity': 'medium',
                'detail': 'Company not found or low confidence match in registry'
            })
        
        # Salary anomaly
        if signals.get('salary_anomaly_score', 0) > 30:
            explanations.append({
                'factor': 'Salary Anomaly Detected',
                'severity': 'medium',
                'detail': 'Offered salary significantly deviates from market standards'
            })
        
        # Recruiter trust
        if signals.get('recruiter_trust_score', 100) < 40:
            explanations.append({
                'factor': 'Recruiter Credibility Issue',
                'severity': 'medium',
                'detail': 'Recruiter using suspicious contact methods or unverified identity'
            })
        
        return explanations
