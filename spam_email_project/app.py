from flask import Flask, render_template, request, jsonify
import re
import os
import sqlite3

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Global variables for ML model and database path
ml_vectorizer = None
ml_model = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'email_project.sqlite')

def init_ml_model():
    """Train a simple machine learning model for spam detection if needed."""
    global ml_vectorizer, ml_model
    if ml_vectorizer is not None and ml_model is not None:
        return

    # Sample training data: 1 = spam, 0 = ham
    training_texts = [
        "Congratulations, you have won a lottery prize, click here now to claim cash",
        "WIN MONEY NOW!!! FREE PRIZE!!!",
        "Urgent: Your account will be closed, act immediately and send your bank details",
        "Limited time offer, risk free bonus, claim your cash reward today",
        "Meeting scheduled for tomorrow at 10am, please confirm your attendance",
        "Weekly newsletter about our products and services",
        "Project update about repository changes and code review meeting",
        "Family dinner this weekend, let me know if you can come",
    ]
    training_labels = [1, 1, 1, 1, 0, 0, 0, 0]

    ml_vectorizer = TfidfVectorizer(stop_words="english")
    X = ml_vectorizer.fit_transform(training_texts)

    ml_model = LogisticRegression()
    ml_model.fit(X, training_labels)

def init_db():
    """Initialize SQLite database and create table if it does not exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS email_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            body TEXT,
            is_spam INTEGER,
            spam_score REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()

def save_email_to_db(subject, body, is_spam_result, spam_score):
    """Save email classification result into the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO email_logs (subject, body, is_spam, spam_score) VALUES (?, ?, ?, ?)",
        (subject, body, int(is_spam_result), float(spam_score)),
    )
    conn.commit()
    conn.close()

def get_email_logs(limit=50):
    """Retrieve recent email classification logs from the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, subject, body, is_spam, spam_score, created_at
        FROM email_logs
        ORDER BY created_at DESC, id DESC
        LIMIT ?
        """,
        (limit,),
    )
    rows = cursor.fetchall()
    conn.close()
    logs = []
    for row in rows:
        logs.append(
            {
                "id": row[0],
                "subject": row[1],
                "body": row[2],
                "is_spam": bool(row[3]),
                "spam_score": row[4],
                "created_at": row[5],
            }
        )
    return logs

def calculate_spam_score(text, spam_indicators):
    """Calculate a spam score based on various indicators"""
    score = 0
    text_lower = text.lower()
    
    # Check for spam keywords
    for keyword, weight in spam_indicators['keywords'].items():
        if keyword in text_lower:
            score += weight
    
    # Check for excessive capitalization
    uppercase_chars = sum(1 for c in text if c.isupper())
    if len(text) > 0:
        uppercase_ratio = uppercase_chars / len(text)
        if uppercase_ratio > 0.3:  # More than 30% uppercase
            score += 5
    
    # Check for excessive exclamation marks
    exclamation_count = text.count('!')
    if exclamation_count > 3:
        score += exclamation_count
    
    # Check for suspicious patterns
    if re.search(r'\d{4,}', text):  # Long sequences of numbers
        score += 3
    
    if re.search(r'\$+|€+|£+', text):  # Currency symbols
        score += 3
    
    # Check for urgency words
    for word in spam_indicators['urgency_words']:
        if word in text_lower:
            score += 2
    
    return max(0, score)  # Ensure non-negative score

def is_spam(subject, body):
    """Spam detection using a machine learning model."""
    if ml_vectorizer is None or ml_model is None:
        init_ml_model()

    full_text = (subject + ' ' + body).strip()
    if not full_text:
        return False, 0.0

    features = ml_vectorizer.transform([full_text])
    spam_proba = ml_model.predict_proba(features)[0][1]
    spam_score = round(float(spam_proba) * 100, 2)
    is_spam_result = spam_proba >= 0.5

    return is_spam_result, spam_score

def get_spam_indicators(subject, body):
    """Get detailed information about what triggered spam detection"""
    indicators = []
    combined_text = (subject + ' ' + body)
    text_lower = combined_text.lower()
    
    spam_keywords = ['win', 'free', 'urgent', 'guaranteed', 'lottery', 'money', 'prize', 
                    'cash', 'congratulations', 'winner', 'bonus', 'click here', 'act now', 
                    'limited time', 'risk free', 'satisfaction guaranteed']
    
    urgency_words = ['immediately', 'now', 'today', 'instant', 'hurry', 
                    'limited', 'expires', 'last chance']
    
    # Check for spam keywords
    for keyword in spam_keywords:
        if keyword in text_lower:
            indicators.append(f"Keyword '{keyword}' found")
    
    # Check for urgency words
    for word in urgency_words:
        if word in text_lower:
            indicators.append(f"Urgency word '{word}' found")
    
    # Check for excessive exclamation marks
    exclamation_count = combined_text.count('!')
    if exclamation_count > 3:
        indicators.append(f"{exclamation_count} exclamation marks found")
    
    # Check for excessive capitalization
    if len(combined_text) > 0:
        uppercase_ratio = sum(1 for c in combined_text if c.isupper()) / len(combined_text)
        if uppercase_ratio > 0.3:
            indicators.append(f"High capitalization ({uppercase_ratio:.1%})")
    
    return indicators

# Configure Flask to look for templates in the correct directory
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template')
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template', 'static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Initialize database and machine learning model at startup
init_db()
init_ml_model()

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    spam_score = None
    indicators = None
    
    if request.method == 'POST':
        subject = request.form.get('subject', '').strip()
        body = request.form.get('body', '').strip()
        
        if subject or body:  # Only process if we have content
            is_spam_result, spam_score = is_spam(subject, body)
            # Save the result in the SQLite database
            save_email_to_db(subject, body, is_spam_result, spam_score)
            if is_spam_result:
                result = "Spam Detected!"
            else:
                result = "This email is NOT spam."
            
            # Get detailed indicators
            indicators = get_spam_indicators(subject, body)
        else:
            result = "Please enter email subject and/or body."
    
    return render_template('index.html', 
                         result=result, 
                         spam_score=spam_score,
                         indicators=indicators)

@app.route('/logs')
def view_logs():
    logs = get_email_logs(limit=50)
    return render_template('logs.html', logs=logs)

@app.route('/api/check_spam', methods=['POST'])
def api_check_spam():
    """API endpoint for spam checking"""
    try:
        data = request.get_json()
        subject = data.get('subject', '').strip()
        body = data.get('body', '').strip()
        
        if not subject and not body:
            return jsonify({'error': 'Subject or body is required'}), 400
        
        is_spam_result, spam_score = is_spam(subject, body)
        indicators = get_spam_indicators(subject, body)
        save_email_to_db(subject, body, is_spam_result, spam_score)
        
        return jsonify({
            'is_spam': is_spam_result,
            'spam_score': spam_score,
            'indicators': indicators
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)