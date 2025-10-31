# Spam Email Detector

A Flask-based web application for detecting spam emails using advanced content analysis.

## Features

- Analyzes email subject and body for spam characteristics
- Provides detailed spam score and indicators
- User-friendly web interface
- REST API endpoint for integration

## Enhanced Spam Detection

The spam detection algorithm analyzes multiple factors:

1. **Keyword Analysis**: Looks for common spam keywords with weighted scoring
2. **Urgency Detection**: Identifies urgency-related language
3. **Formatting Analysis**: Detects excessive capitalization and exclamation marks
4. **Pattern Recognition**: Finds suspicious numerical patterns and currency symbols

## Installation

1. Ensure Python 3.6+ is installed
2. Install required dependencies:
   ```
   pip install flask
   ```

## Running the Application

### Method 1: Using the batch file (Windows)
```
run_app.bat
```

### Method 2: Using Python directly
```
python app.py
```

### Method 3: Using Flask CLI
```
set FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5000
```

## Usage

1. Open your web browser and navigate to `http://localhost:5000`
2. Enter the email subject and body in the provided form
3. Click "Check Email" to analyze the content
4. View the spam detection results with detailed indicators

## API Endpoint

The application also provides a REST API for integration:

```
POST /api/check_spam
Content-Type: application/json

{
  "subject": "Email subject",
  "body": "Email body content"
}
```

Response:
```json
{
  "is_spam": true/false,
  "spam_score": 25,
  "indicators": [
    "Keyword 'free' found",
    "Keyword 'win' found",
    "5 exclamation marks found"
  ]
}
```

## How It Works

The spam detection algorithm uses a weighted scoring system:

- Spam keywords: 5-10 points each
- Urgency words: 2 points each
- Excessive exclamation marks: 1 point each
- High capitalization: 5 points
- Suspicious patterns: 3 points each

If the total score exceeds 15, the email is classified as spam.