import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, f1_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib
import os
import re

class MLScamClassifier:
    """Advanced multi-model scam classification system with enhanced features"""
    
    def __init__(self):
        # Enhanced TF-IDF with better parameters
        self.vectorizer = TfidfVectorizer(
            max_features=2000,
            ngram_range=(1, 3),  # Unigrams, bigrams, and trigrams
            min_df=2,
            max_df=0.8,
            sublinear_tf=True,
            use_idf=True
        )
        self.models = {}
        self.best_model = None
        self.best_model_name = None
        self.ensemble_model = None
        self.model_dir = 'models/saved'
        os.makedirs(self.model_dir, exist_ok=True)
        
        # Scam keywords for feature engineering
        self.scam_keywords = {
            'payment': ['pay', 'fee', 'registration', 'processing', 'verification', 'deposit', 'charges', 'wallet', 'transfer', 'send money'],
            'urgency': ['urgent', 'immediately', 'hurry', 'limited time', 'expires', 'last chance', 'act now', 'closing soon', 'final call'],
            'contact': ['whatsapp only', 'telegram only', 'no email', 'no calls', 'contact via whatsapp'],
            'selection': ['no interview', 'direct selection', 'selected without', 'hired without', 'guaranteed'],
            'money': ['earn lakhs', 'work from home', 'easy money', 'guaranteed income', 'lpa for freshers'],
            'suspicious': ['congratulations', 'selected', 'hired', 'won', 'lottery']
        }
    
    def extract_advanced_features(self, texts):
        """Extract advanced features from texts"""
        features = []
        
        for text in texts:
            text_lower = text.lower()
            feat = {}
            
            # Keyword category counts
            for category, keywords in self.scam_keywords.items():
                feat[f'{category}_count'] = sum(1 for kw in keywords if kw in text_lower)
            
            # Text statistics
            feat['text_length'] = len(text)
            feat['word_count'] = len(text.split())
            feat['avg_word_length'] = np.mean([len(word) for word in text.split()]) if text.split() else 0
            feat['exclamation_count'] = text.count('!')
            feat['question_count'] = text.count('?')
            feat['uppercase_ratio'] = sum(1 for c in text if c.isupper()) / len(text) if text else 0
            feat['digit_ratio'] = sum(1 for c in text if c.isdigit()) / len(text) if text else 0
            
            # Specific pattern detection
            feat['has_rupee_symbol'] = 1 if 'rs' in text_lower or '₹' in text else 0
            feat['has_phone_number'] = 1 if re.search(r'\+?\d{10,}', text) else 0
            feat['has_lpa_mention'] = 1 if 'lpa' in text_lower else 0
            feat['has_salary_range'] = 1 if re.search(r'\d+\s*-\s*\d+\s*lpa', text_lower) else 0
            
            features.append(feat)
        
        return pd.DataFrame(features)
    
    def train_models(self, texts, labels):
        """Train multiple advanced classifiers with hyperparameter tuning"""
        # Vectorize text
        X_text = self.vectorizer.fit_transform(texts)
        
        # Extract advanced features
        X_advanced = self.extract_advanced_features(texts)
        
        # Combine features
        from scipy.sparse import hstack
        X = hstack([X_text, X_advanced.values])
        y = np.array(labels)
        
        # Split data with stratification
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Define optimized models
        model_configs = {
            'Logistic Regression': LogisticRegression(
                max_iter=2000,
                C=1.0,
                class_weight='balanced',
                random_state=42
            ),
            'Random Forest': RandomForestClassifier(
                n_estimators=200,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                class_weight='balanced',
                random_state=42
            ),
            'Gradient Boosting': GradientBoostingClassifier(
                n_estimators=150,
                learning_rate=0.1,
                max_depth=5,
                min_samples_split=5,
                random_state=42
            ),
            'SVM': SVC(
                kernel='rbf',
                C=1.0,
                gamma='scale',
                class_weight='balanced',
                probability=True,
                random_state=42
            )
        }
        
        results = {}
        best_f1 = 0
        
        # Train and evaluate each model
        for name, model in model_configs.items():
            print(f"Training {name}...")
            model.fit(X_train, y_train)
            
            # Predictions
            y_pred = model.predict(X_test)
            y_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
            
            # Cross-validation
            cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='f1')
            f1 = f1_score(y_test, y_pred)
            
            results[name] = {
                'model': model,
                'cv_f1_mean': cv_scores.mean(),
                'cv_f1_std': cv_scores.std(),
                'test_f1': f1,
                'test_predictions': y_pred,
                'test_probabilities': y_proba
            }
            
            print(f"{name} - CV F1: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f}), Test F1: {f1:.4f}")
            
            if cv_scores.mean() > best_f1:
                best_f1 = cv_scores.mean()
                self.best_model = model
                self.best_model_name = name
        
        # Create ensemble model (Voting Classifier)
        print("\nCreating Ensemble Model...")
        ensemble_models = [(name, res['model']) for name, res in results.items()]
        self.ensemble_model = VotingClassifier(
            estimators=ensemble_models,
            voting='soft',
            weights=[2, 3, 3, 2]  # Give more weight to RF and GB
        )
        self.ensemble_model.fit(X_train, y_train)
        
        # Evaluate ensemble
        ensemble_pred = self.ensemble_model.predict(X_test)
        ensemble_f1 = f1_score(y_test, ensemble_pred)
        print(f"Ensemble Model - Test F1: {ensemble_f1:.4f}")
        
        # Use ensemble if it's better
        if ensemble_f1 > best_f1:
            self.best_model = self.ensemble_model
            self.best_model_name = "Ensemble (Voting)"
            print(f"\nBest model: Ensemble (F1: {ensemble_f1:.4f})")
        else:
            print(f"\nBest model: {self.best_model_name} (F1: {best_f1:.4f})")
        
        self.models = {name: res['model'] for name, res in results.items()}
        
        # Save models
        self.save_models()
        
        return results
    
    def predict(self, text):
        """Predict scam probability for text with spam line detection"""
        if self.best_model is None:
            return {
                'is_scam': False,
                'probability': 50.0,
                'confidence': 'low',
                'model': 'default',
                'spam_lines': []
            }
        
        # Vectorize
        X_text = self.vectorizer.transform([text])
        
        # Extract advanced features
        X_advanced = self.extract_advanced_features([text])
        
        # Combine features
        from scipy.sparse import hstack
        X = hstack([X_text, X_advanced.values])
        
        # Predict
        prediction = self.best_model.predict(X)[0]
        
        if hasattr(self.best_model, 'predict_proba'):
            probability = self.best_model.predict_proba(X)[0][1] * 100
        else:
            probability = 75.0 if prediction == 1 else 25.0
        
        confidence = self._get_confidence_level(probability)
        
        # Detect spam lines
        spam_lines = self._detect_spam_lines(text)
        
        return {
            'is_scam': bool(prediction),
            'probability': round(probability, 2),
            'confidence': confidence,
            'model': self.best_model_name,
            'spam_lines': spam_lines
        }
    
    def _detect_spam_lines(self, text):
        """Detect specific spam/scam lines in the text"""
        spam_lines = []
        lines = text.split('\n')
        
        for line in lines:
            line_lower = line.strip().lower()
            if not line_lower:
                continue
            
            # Check for scam patterns
            scam_score = 0
            matched_patterns = []
            
            for category, keywords in self.scam_keywords.items():
                for keyword in keywords:
                    if keyword in line_lower:
                        scam_score += 1
                        matched_patterns.append(keyword)
            
            # If line has multiple scam keywords, mark it as spam
            if scam_score >= 2:
                spam_lines.append({
                    'line': line.strip(),
                    'score': scam_score,
                    'patterns': matched_patterns
                })
        
        # Sort by score (most suspicious first)
        spam_lines.sort(key=lambda x: x['score'], reverse=True)
        
        return spam_lines[:10]  # Return top 10 spam lines
    
    def _get_confidence_level(self, probability):
        """Get confidence level from probability"""
        if probability > 85 or probability < 15:
            return 'high'
        elif probability > 65 or probability < 35:
            return 'medium'
        else:
            return 'low'
    
    def save_models(self):
        """Save trained models and vectorizer"""
        joblib.dump(self.vectorizer, os.path.join(self.model_dir, 'vectorizer.pkl'))
        joblib.dump(self.best_model, os.path.join(self.model_dir, 'best_model.pkl'))
        joblib.dump(self.best_model_name, os.path.join(self.model_dir, 'best_model_name.pkl'))
        if self.ensemble_model:
            joblib.dump(self.ensemble_model, os.path.join(self.model_dir, 'ensemble_model.pkl'))
        print(f"Models saved to {self.model_dir}")
    
    def load_models(self):
        """Load trained models"""
        try:
            self.vectorizer = joblib.load(os.path.join(self.model_dir, 'vectorizer.pkl'))
            self.best_model = joblib.load(os.path.join(self.model_dir, 'best_model.pkl'))
            self.best_model_name = joblib.load(os.path.join(self.model_dir, 'best_model_name.pkl'))
            try:
                self.ensemble_model = joblib.load(os.path.join(self.model_dir, 'ensemble_model.pkl'))
            except:
                pass
            print(f"Models loaded: {self.best_model_name}")
            return True
        except:
            print("No saved models found. Using default predictions.")
            return False
