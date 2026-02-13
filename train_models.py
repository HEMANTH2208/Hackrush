"""
Standalone script to train ML models
Run this before starting the Flask app
"""

from models.ml_classifier import MLScamClassifier
from data.sample_dataset import get_training_data

def main():
    print("=" * 60)
    print("JobShield AI - Model Training")
    print("=" * 60)
    
    # Initialize classifier
    classifier = MLScamClassifier()
    
    # Load training data
    print("\nLoading training data...")
    texts, labels = get_training_data()
    print(f"Loaded {len(texts)} samples")
    print(f"Scam samples: {sum(labels)}")
    print(f"Legitimate samples: {len(labels) - sum(labels)}")
    
    # Train models
    print("\nTraining multiple classifiers...")
    print("-" * 60)
    results = classifier.train_models(texts, labels)
    
    print("\n" + "=" * 60)
    print("Training Complete!")
    print(f"Best Model: {classifier.best_model_name}")
    print("=" * 60)
    
    # Test predictions
    print("\nTesting predictions on sample texts...")
    test_samples = [
        "Congratulations! Pay Rs 2000 fee. Join via WhatsApp immediately.",
        "We invite you for interview at our office next Monday."
    ]
    
    for i, text in enumerate(test_samples, 1):
        result = classifier.predict(text)
        print(f"\nSample {i}: {text[:60]}...")
        print(f"Prediction: {'SCAM' if result['is_scam'] else 'LEGITIMATE'}")
        print(f"Probability: {result['probability']:.2f}%")
        print(f"Confidence: {result['confidence']}")

if __name__ == '__main__':
    main()
