from app import is_spam, get_spam_indicators

# Test cases
test_cases = [
    {
        'subject': 'Congratulations! You\'ve won $1000!',
        'body': 'Click here now to claim your prize! Limited time offer! Act immediately!'
    },
    {
        'subject': 'Meeting scheduled for tomorrow',
        'body': 'Hi team, just confirming our meeting scheduled for tomorrow at 10am.'
    },
    {
        'subject': 'URGENT: Your account will be closed!',
        'body': 'WIN MONEY NOW!!! FREE PRIZE!!!'
    },
    {
        'subject': 'Weekly newsletter',
        'body': 'Here is your weekly update on our products and services.'
    }
]

print("Testing Spam Detector")
print("=" * 50)

for i, test in enumerate(test_cases, 1):
    subject = test['subject']
    body = test['body']
    
    print(f"\nTest Case {i}:")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
    
    is_spam_result, spam_score = is_spam(subject, body)
    indicators = get_spam_indicators(subject, body)
    
    print(f"Spam Detected: {'Yes' if is_spam_result else 'No'}")
    print(f"Spam Score: {spam_score}")
    print("Indicators:")
    for indicator in indicators:
        print(f"  - {indicator}")
    print("-" * 30)