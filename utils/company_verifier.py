import requests
import re
from urllib.parse import quote

class CompanyVerifier:
    """Company legitimacy verification using OpenCorporates API"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_url = "https://api.opencorporates.com/v0.4"
    
    def verify_company(self, company_name, jurisdiction=None):
        """Verify company existence and legitimacy"""
        try:
            # Search for company
            search_url = f"{self.base_url}/companies/search"
            params = {
                'q': company_name,
                'per_page': 5
            }
            
            if self.api_key:
                params['api_token'] = self.api_key
            
            if jurisdiction:
                params['jurisdiction_code'] = jurisdiction
            
            response = requests.get(search_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                companies = data.get('results', {}).get('companies', [])
                
                if companies:
                    best_match = companies[0]['company']
                    return {
                        'found': True,
                        'confidence': self._calculate_confidence(company_name, best_match),
                        'company_name': best_match.get('name'),
                        'jurisdiction': best_match.get('jurisdiction_code'),
                        'status': best_match.get('current_status'),
                        'incorporation_date': best_match.get('incorporation_date'),
                        'company_number': best_match.get('company_number'),
                        'address': best_match.get('registered_address_in_full')
                    }
                else:
                    return {
                        'found': False,
                        'confidence': 0,
                        'message': 'Company not found in registry'
                    }
            else:
                return {
                    'found': False,
                    'confidence': 0,
                    'message': 'API request failed'
                }
        
        except Exception as e:
            return {
                'found': False,
                'confidence': 0,
                'message': f'Verification error: {str(e)}'
            }
    
    def _calculate_confidence(self, search_name, company_data):
        """Calculate confidence score based on name match"""
        search_name_clean = re.sub(r'[^\w\s]', '', search_name.lower())
        company_name_clean = re.sub(r'[^\w\s]', '', company_data.get('name', '').lower())
        
        # Simple similarity check
        if search_name_clean == company_name_clean:
            confidence = 95
        elif search_name_clean in company_name_clean or company_name_clean in search_name_clean:
            confidence = 75
        else:
            confidence = 50
        
        # Adjust based on status
        status = company_data.get('current_status', '').lower()
        if 'active' in status:
            confidence += 5
        elif 'inactive' in status or 'dissolved' in status:
            confidence -= 20
        
        return min(max(confidence, 0), 100)
    
    def verify_email_domain(self, email, company_name):
        """Check if email domain matches company name"""
        try:
            domain = email.split('@')[1].lower()
            company_clean = re.sub(r'[^\w]', '', company_name.lower())
            
            # Check if company name is in domain
            if company_clean in domain.replace('.', ''):
                return {
                    'match': True,
                    'confidence': 80,
                    'domain': domain
                }
            elif domain in ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']:
                return {
                    'match': False,
                    'confidence': 20,
                    'domain': domain,
                    'warning': 'Using generic email provider'
                }
            else:
                return {
                    'match': False,
                    'confidence': 40,
                    'domain': domain
                }
        except:
            return {
                'match': False,
                'confidence': 0,
                'domain': None
            }
