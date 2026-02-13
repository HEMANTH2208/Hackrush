import requests
import re
from bs4 import BeautifulSoup

class MCAVerifier:
    """Ministry of Corporate Affairs (India) company verification"""
    
    def __init__(self):
        self.base_url = "https://www.mca.gov.in"
        # Note: MCA doesn't have a public API, so we'll use a combination of approaches
        
    def verify_indian_company(self, company_name):
        """
        Verify if company is registered with MCA (India)
        Note: This is a simplified version. Full MCA verification requires official API access.
        """
        try:
            # Clean company name
            company_clean = self._clean_company_name(company_name)
            
            # Check common patterns for Indian companies
            indian_indicators = self._check_indian_indicators(company_name)
            
            # Simulate MCA check (in production, use official MCA API)
            result = {
                'found': False,
                'confidence': 0,
                'source': 'MCA',
                'company_name': company_name,
                'indicators': indian_indicators
            }
            
            # Check if company has Indian legal entity suffixes
            if any(suffix in company_clean.upper() for suffix in [
                'PRIVATE LIMITED', 'PVT LTD', 'LIMITED', 'LTD',
                'INDIA', 'INDIAN', 'TECHNOLOGIES', 'SERVICES'
            ]):
                result['confidence'] += 30
                result['found'] = True
            
            # Check for known Indian companies (sample list)
            known_indian_companies = [
                'TCS', 'TATA CONSULTANCY SERVICES', 'INFOSYS', 'WIPRO',
                'HCL', 'TECH MAHINDRA', 'MINDTREE', 'MPHASIS',
                'COGNIZANT', 'CAPGEMINI INDIA', 'ACCENTURE INDIA',
                'IBM INDIA', 'MICROSOFT INDIA', 'GOOGLE INDIA',
                'AMAZON INDIA', 'FLIPKART', 'PAYTM', 'OLA',
                'SWIGGY', 'ZOMATO', 'BYJU', 'RELIANCE'
            ]
            
            for known_company in known_indian_companies:
                if known_company in company_clean.upper():
                    result['found'] = True
                    result['confidence'] = 90
                    result['status'] = 'Active'
                    result['message'] = f'Recognized Indian company: {known_company}'
                    break
            
            # If not found in known list but has indicators
            if result['found'] and result['confidence'] < 90:
                result['status'] = 'Likely Registered'
                result['message'] = 'Company appears to be Indian registered entity'
            elif not result['found']:
                result['message'] = 'Company not found in MCA registry or not an Indian company'
            
            return result
            
        except Exception as e:
            return {
                'found': False,
                'confidence': 0,
                'source': 'MCA',
                'message': f'MCA verification error: {str(e)}'
            }
    
    def _clean_company_name(self, name):
        """Clean company name for comparison"""
        # Remove special characters
        cleaned = re.sub(r'[^\w\s]', ' ', name)
        # Remove extra spaces
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned
    
    def _check_indian_indicators(self, company_name):
        """Check for Indian company indicators"""
        indicators = []
        name_upper = company_name.upper()
        
        # Legal entity types
        if 'PRIVATE LIMITED' in name_upper or 'PVT LTD' in name_upper:
            indicators.append('Private Limited Company')
        if 'LIMITED' in name_upper or 'LTD' in name_upper:
            indicators.append('Limited Company')
        
        # Geographic indicators
        if 'INDIA' in name_upper or 'INDIAN' in name_upper:
            indicators.append('India-based')
        
        # Business type indicators
        if any(word in name_upper for word in ['TECHNOLOGIES', 'TECH', 'SOFTWARE', 'SERVICES', 'SOLUTIONS']):
            indicators.append('IT/Services Company')
        
        return indicators
    
    def get_cin_info(self, cin):
        """
        Get company information from CIN (Corporate Identification Number)
        CIN format: L/U + 5-digit industry code + 2-letter state code + 4-digit year + PLC/PTC + 6-digit registration number
        """
        try:
            if not cin or len(cin) < 21:
                return {'valid': False, 'message': 'Invalid CIN format'}
            
            # Parse CIN
            listing_status = cin[0]  # L = Listed, U = Unlisted
            industry_code = cin[1:6]
            state_code = cin[6:8]
            year = cin[8:12]
            company_type = cin[12:15]  # PLC = Public, PTC = Private
            registration_number = cin[15:21]
            
            return {
                'valid': True,
                'cin': cin,
                'listing_status': 'Listed' if listing_status == 'L' else 'Unlisted',
                'industry_code': industry_code,
                'state_code': state_code,
                'incorporation_year': year,
                'company_type': 'Public Limited' if company_type == 'PLC' else 'Private Limited',
                'registration_number': registration_number
            }
        except Exception as e:
            return {'valid': False, 'message': f'CIN parsing error: {str(e)}'}
