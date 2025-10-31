from flask import Flask, render_template, request, jsonify
import re
import os

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
    """Enhanced spam detection with scoring system"""
    # Define spam indicators with weights
    spam_indicators = {
        'keywords': {
            'win': 10, 'free': 8, 'urgent': 7, 'guaranteed': 6, 
            'lottery': 9, 'money': 7, 'prize': 8, 'cash': 6,
            'congratulations': 5, 'winner': 8, 'bonus': 6,
            'click here': 7, 'act now': 8, 'limited time': 6,
            'risk free': 5, 'satisfaction guaranteed': 5
        },
        'urgency_words': [
            'immediately', 'now', 'today', 'instant', 'hurry', 
            'limited', 'expires', 'last chance'
        ]
    }
    
    # Combine subject and body for analysis
    full_text = (subject + ' ' + body).strip()
    
    # Calculate spam score
    spam_score = calculate_spam_score(full_text, spam_indicators)
    
    # Determine if spam based on threshold
    spam_threshold = 15
    
    return spam_score >= spam_threshold, spam_score

def get_spam_indicators(subject, body):
    """Get detailed information about what triggered spam detection"""
    indicators = []
    text = (subject + ' ' + body).lower()
    
    spam_keywords = ['win', 'free', 'urgent', 'guaranteed', 'lottery', 'money', 'prize', 
                    'cash', 'congratulations', 'winner', 'bonus', 'click here', 'act now', 
                    'limited time', 'risk free', 'satisfaction guaranteed']
    
    urgency_words = ['immediately', 'now', 'today', 'instant', 'hurry', 
                    'limited', 'expires', 'last chance']
    
    # Check for spam keywords
    for keyword in spam_keywords:
        if keyword in text:
            indicators.append(f"Keyword '{keyword}' found")
    
    # Check for urgency words
    for word in urgency_words:
        if word in text:
            indicators.append(f"Urgency word '{word}' found")
    
    # Check for excessive exclamation marks
    if text.count('!') > 3:
        indicators.append(f"{text.count('!')} exclamation marks found")
    
    # Check for excessive capitalization
    if len(text) > 0:
        uppercase_ratio = sum(1 for c in text if c.isupper()) / len(text)
        if uppercase_ratio > 0.3:
            indicators.append(f"High capitalization ({uppercase_ratio:.1%})")
    
    return indicators

# Configure Flask to look for templates in the correct directory
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template')
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template', 'static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

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
        
        return jsonify({
            'is_spam': is_spam_result,
            'spam_score': spam_score,
            'indicators': indicators
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)