class FraudRuleEngine:
    """Deterministic fraud detection rules"""
    
    def __init__(self):
        self.scam_patterns = {
            'payment_request': [
                'pay registration fee',
                'interview fee',
                'processing fee',
                'deposit required',
                'send money',
                'wallet transfer'
            ],
            'instant_offer': [
                'instant offer',
                'no interview',
                'selected without',
                'congratulations you are selected'
            ],
            'urgency': [
                'join within 24 hours',
                'urgent joining',
                'immediate start',
                'offer expires today'
            ],
            'suspicious_contact': [
                'whatsapp only',
                'telegram only',
                'contact via whatsapp',
                'no email communication'
            ],
            'unrealistic_salary': [
                'earn lakhs',
                'guaranteed income',
                'no work high pay',
                'easy money'
            ]
        }
    
    def check_rules(self, text):
        """Check text against fraud rules"""
        text_lower = text.lower()
        triggered_rules = []
        rule_score = 0
        
        for category, patterns in self.scam_patterns.items():
            for pattern in patterns:
                if pattern in text_lower:
                    triggered_rules.append({
                        'category': category,
                        'pattern': pattern,
                        'severity': self._get_severity(category)
                    })
                    rule_score += self._get_severity(category)
        
        return {
            'triggered_rules': triggered_rules,
            'rule_score': min(rule_score, 100),
            'high_confidence_scam': rule_score >= 50
        }
    
    def _get_severity(self, category):
        """Get severity score for each category"""
        severity_map = {
            'payment_request': 30,
            'instant_offer': 20,
            'urgency': 15,
            'suspicious_contact': 20,
            'unrealistic_salary': 15
        }
        return severity_map.get(category, 10)
    
    def get_evidence(self, text, triggered_rules):
        """Highlight suspicious phrases in text"""
        evidence = []
        for rule in triggered_rules:
            pattern = rule['pattern']
            if pattern in text.lower():
                evidence.append({
                    'phrase': pattern,
                    'category': rule['category'],
                    'severity': rule['severity']
                })
        return evidence
