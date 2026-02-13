import re

class RecruiterScorer:
    """Score recruiter credibility and trust"""
    
    def __init__(self):
        self.trusted_domains = [
            'company.com', 'corp.com', 'inc.com', 'ltd.com'
        ]
        self.suspicious_domains = [
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
            'protonmail.com', 'tempmail.com'
        ]
    
    def score_recruiter(self, email=None, contact_method=None, linkedin_url=None):
        """Calculate recruiter trust score"""
        trust_score = 50  # Base score
        factors = []
        
        # Email domain analysis
        if email:
            domain_score, domain_factor = self._score_email_domain(email)
            trust_score += domain_score
            if domain_factor:
                factors.append(domain_factor)
        
        # Contact method analysis
        if contact_method:
            contact_score, contact_factor = self._score_contact_method(contact_method)
            trust_score += contact_score
            if contact_factor:
                factors.append(contact_factor)
        
        # LinkedIn profile analysis
        if linkedin_url:
            linkedin_score, linkedin_factor = self._score_linkedin(linkedin_url)
            trust_score += linkedin_score
            if linkedin_factor:
                factors.append(linkedin_factor)
        
        # Normalize score
        trust_score = max(0, min(100, trust_score))
        
        return {
            'trust_score': trust_score,
            'trust_level': self._get_trust_level(trust_score),
            'factors': factors
        }
    
    def _score_email_domain(self, email):
        """Score email domain credibility"""
        try:
            domain = email.split('@')[1].lower()
            
            if domain in self.suspicious_domains:
                return -20, {
                    'factor': 'Email Domain',
                    'impact': 'negative',
                    'detail': f'Using generic email provider ({domain})'
                }
            elif any(trusted in domain for trusted in self.trusted_domains):
                return 20, {
                    'factor': 'Email Domain',
                    'impact': 'positive',
                    'detail': 'Using corporate email domain'
                }
            else:
                return 10, {
                    'factor': 'Email Domain',
                    'impact': 'neutral',
                    'detail': f'Using custom domain ({domain})'
                }
        except:
            return -10, {
                'factor': 'Email Domain',
                'impact': 'negative',
                'detail': 'Invalid email format'
            }
    
    def _score_contact_method(self, method):
        """Score contact method"""
        method_lower = method.lower()
        
        if 'whatsapp' in method_lower or 'telegram' in method_lower:
            return -25, {
                'factor': 'Contact Method',
                'impact': 'negative',
                'detail': 'Using informal messaging apps only'
            }
        elif 'email' in method_lower:
            return 15, {
                'factor': 'Contact Method',
                'impact': 'positive',
                'detail': 'Using professional email communication'
            }
        elif 'phone' in method_lower:
            return 10, {
                'factor': 'Contact Method',
                'impact': 'neutral',
                'detail': 'Using phone communication'
            }
        else:
            return 0, None
    
    def _score_linkedin(self, linkedin_url):
        """Score LinkedIn profile presence"""
        if not linkedin_url or linkedin_url.strip() == '':
            return -10, {
                'factor': 'LinkedIn Profile',
                'impact': 'negative',
                'detail': 'No LinkedIn profile provided'
            }
        
        # Basic URL validation
        if 'linkedin.com/in/' in linkedin_url.lower():
            return 20, {
                'factor': 'LinkedIn Profile',
                'impact': 'positive',
                'detail': 'LinkedIn profile provided'
            }
        else:
            return -5, {
                'factor': 'LinkedIn Profile',
                'impact': 'negative',
                'detail': 'Invalid LinkedIn URL format'
            }
    
    def _get_trust_level(self, score):
        """Get trust level from score"""
        if score >= 70:
            return 'HIGH_TRUST'
        elif score >= 50:
            return 'MODERATE_TRUST'
        elif score >= 30:
            return 'LOW_TRUST'
        else:
            return 'UNTRUSTED'
