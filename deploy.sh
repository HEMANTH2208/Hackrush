#!/bin/bash

echo "================================"
echo "JobShield AI - Deployment Script"
echo "================================"

# Create necessary directories
echo "Creating directories..."
mkdir -p models/saved
mkdir -p reports
mkdir -p static/css
mkdir -p static/js
mkdir -p templates
mkdir -p utils
mkdir -p data

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Download NLTK data
echo "Downloading NLTK data..."
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"

# Train models
echo "Training ML models..."
python train_models.py

echo ""
echo "================================"
echo "Deployment Complete!"
echo "================================"
echo ""
echo "To start the application:"
echo "  python app.py"
echo ""
echo "Then open: http://localhost:5000"
echo "================================"
