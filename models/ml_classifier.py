import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import joblib
import os

class MLScamClassifier:
    """Multi-model scam classification system"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))
        self.models = {}
        self.best_model = None
        self.best_model_name = None
        self.model_dir = 'models/saved'
        os.makedirs(self.model_dir, exist_ok=True)
    
    def train_models(self, texts, labels):
        """Train multiple classifiers and select best"""
        # Vectorize text
        X = self.vectorizer.fit_transform(texts)
        y = np.array(labels)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Define models
        model_configs = {
            'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
            'Decision Tree': DecisionTreeClassifier(max_depth=10, random_state=42),
            'KNN': KNeighborsClassifier(n_neighbors=5),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42)
        }
        
        results = {}
        
        # Train and evaluate each model
        for name, model in model_configs.items():
            print(f"Training {name}...")
            model.fit(X_train, y_train)
            
            # Predictions
            y_pred = model.predict(X_test)
            y_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
            
            # Metrics
            cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='f1')
            
            results[name] = {
                'model': model,
                'cv_f1_mean': cv_scores.mean(),
                'cv_f1_std': cv_scores.std(),
                'test_predictions': y_pred,
                'test_probabilities': y_proba
            }
            
            print(f"{name} - CV F1: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
        
        # Select best model based on CV F1 score
        best_name = max(results, key=lambda x: results[x]['cv_f1_mean'])
        self.best_model = results[best_name]['model']
        self.best_model_name = best_name
        self.models = {name: res['model'] for name, res in results.items()}
        
        print(f"\nBest model: {best_name}")
        
        # Save models
        self.save_models()
        
        return results
    
    def predict(self, text):
        """Predict scam probability for text"""
        if self.best_model is None:
            # Return default prediction if no model trained
            return {
                'is_scam': False,
                'probability': 50.0,
                'confidence': 'low',
                'model': 'default'
            }
        
        # Vectorize
        X = self.vectorizer.transform([text])
        
        # Predict
        prediction = self.best_model.predict(X)[0]
        
        if hasattr(self.best_model, 'predict_proba'):
            probability = self.best_model.predict_proba(X)[0][1] * 100
        else:
            probability = 75.0 if prediction == 1 else 25.0
        
        confidence = self._get_confidence_level(probability)
        
        return {
            'is_scam': bool(prediction),
            'probability': round(probability, 2),
            'confidence': confidence,
            'model': self.best_model_name
        }
    
    def _get_confidence_level(self, probability):
        """Get confidence level from probability"""
        if probability > 80 or probability < 20:
            return 'high'
        elif probability > 60 or probability < 40:
            return 'medium'
        else:
            return 'low'
    
    def save_models(self):
        """Save trained models and vectorizer"""
        joblib.dump(self.vectorizer, os.path.join(self.model_dir, 'vectorizer.pkl'))
        joblib.dump(self.best_model, os.path.join(self.model_dir, 'best_model.pkl'))
        joblib.dump(self.best_model_name, os.path.join(self.model_dir, 'best_model_name.pkl'))
        print(f"Models saved to {self.model_dir}")
    
    def load_models(self):
        """Load trained models"""
        try:
            self.vectorizer = joblib.load(os.path.join(self.model_dir, 'vectorizer.pkl'))
            self.best_model = joblib.load(os.path.join(self.model_dir, 'best_model.pkl'))
            self.best_model_name = joblib.load(os.path.join(self.model_dir, 'best_model_name.pkl'))
            print(f"Models loaded: {self.best_model_name}")
            return True
        except:
            print("No saved models found. Using default predictions.")
            return False
