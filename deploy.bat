@echo off
echo ================================
echo JobShield AI - Deployment Script
echo ================================

REM Create necessary directories
echo Creating directories...
if not exist "models\saved" mkdir models\saved
if not exist "reports" mkdir reports
if not exist "static\css" mkdir static\css
if not exist "static\js" mkdir static\js
if not exist "templates" mkdir templates
if not exist "utils" mkdir utils
if not exist "data" mkdir data

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Download NLTK data
echo Downloading NLTK data...
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"

REM Train models
echo Training ML models...
python train_models.py

echo.
echo ================================
echo Deployment Complete!
echo ================================
echo.
echo To start the application:
echo   python app.py
echo.
echo Then open: http://localhost:5000
echo ================================
pause
