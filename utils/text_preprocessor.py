import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

class TextPreprocessor:
    def __init__(self):
        try:
            self.stop_words = set(stopwords.words('english'))
            self.lemmatizer = WordNetLemmatizer()
        except LookupError:
            nltk.download('stopwords')
            nltk.download('punkt')
            nltk.download('wordnet')
            self.stop_words = set(stopwords.words('english'))
            self.lemmatizer = WordNetLemmatizer()
    
    def clean_text(self, text):
        """Normalize and clean text"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove phone numbers
        text = re.sub(r'\+?\d[\d\s\-\(\)]{7,}\d', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove emojis and special characters
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def tokenize_and_lemmatize(self, text):
        """Tokenize and lemmatize text"""
        tokens = word_tokenize(text)
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens 
                  if token not in self.stop_words and len(token) > 2]
        return tokens
    
    def preprocess(self, text):
        """Full preprocessing pipeline"""
        cleaned = self.clean_text(text)
        tokens = self.tokenize_and_lemmatize(cleaned)
        return ' '.join(tokens)
    
    def extract_features(self, text):
        """Extract risk-related features"""
        features = {}
        text_lower = text.lower()
        
        # Urgency indicators
        urgency_keywords = ['urgent', 'immediate', 'asap', '24 hours', 'today', 'now']
        features['urgency_score'] = sum(1 for kw in urgency_keywords if kw in text_lower)
        
        # Payment indicators
        payment_keywords = ['fee', 'payment', 'deposit', 'registration', 'processing fee', 'wallet']
        features['payment_score'] = sum(1 for kw in payment_keywords if kw in text_lower)
        
        # Unrealistic promises
        promise_keywords = ['guaranteed', 'no experience', 'work from home', 'easy money', 'high salary']
        features['promise_score'] = sum(1 for kw in promise_keywords if kw in text_lower)
        
        return features
