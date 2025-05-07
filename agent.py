from email_reader import get_emails
from email_sender import send_reply
from email_replier import send_authentication_email
from content_classifier import is_essential

EMAIL = "blessoncbiju123@gmail.com"
PASSWORD = "cmbdugbtujkhewpi"

def decide_action(email):
    sender = email["from"]
    subject = email.get("subject", "")
    body = email.get("body", "")
    
    # Clean and combine subject and body for better classification
    subject = subject.strip() if subject else ""
    body = body.strip() if body else ""
    full_content = f"{subject} {body}".lower()  # Convert to lowercase for better matching
    
    print(f"\nProcessing email from: {sender}")
    print(f"Subject: {subject}")
    
    # Direct classification for obviously important emails
    if any(keyword in subject.lower() for keyword in [
        'job', 'career', 'position', 'vacancy', 'analyst', 'developer',
        'selected', 'interview', 'offer', 'opportunity'
    ]):
        print("Important job-related email detected")
        return ("job", sender, subject)
    
    if any(keyword in subject.lower() for keyword in [
        'urgent', 'immediate', 'important', 'action required'
    ]):
        print("Urgent email detected")
        return ("urgent", sender, subject)
    
    if any(keyword in subject.lower() for keyword in [
        'security', 'verification', 'password', 'authentication', 'account'
    ]):
        print("Security-related email detected")
        return ("auth", sender)
    
    if any(keyword in subject.lower() for keyword in [
        'meeting', 'interview', 'zoom', 'discussion'
    ]):
        print("Meeting-related email detected")
        return ("meeting", sender, subject)
    
    # Use ML classifier as backup only if no direct matches found
    if is_essential(full_content):
        print("ML classifier marked this as essential")
        return ("generic", sender, subject)
    
    print("Result: Not essential - Skipping\n")
    return None

def run_agent():
    print("Starting email processing...")
    emails = get_emails(EMAIL, PASSWORD)
    
    print(f"Found {len(emails)} emails to process")
    essential_count = 0
    
    for email in emails:
        action = decide_action(email)
        if action is None:
            continue

        essential_count += 1
        
        if action[0] == "auth":
            print(f"Sending authentication request to {action[1]}")
            send_authentication_email(to_email=action[1], from_email=EMAIL, password=PASSWORD)

        elif action[0] == "job":
            _, to, subject = action
            print(f"Sending job-related response to {to}")
            reply = f"""Hi,

Thank you for considering my application. I'm excited about this opportunity regarding: "{subject}".

I'm available for any interviews or further discussions.

Best regards,
Blesson
"""
            send_reply(EMAIL, PASSWORD, to, f"Re: {subject}", reply)
            
        elif action[0] == "urgent":
            _, to, subject = action
            print(f"Sending urgent response to {to}")
            reply = f"""Hi,

I've received your urgent message regarding: "{subject}" and will address it immediately.

Please expect a response within 2 hours.

Regards,
Blesson
"""
            send_reply(EMAIL, PASSWORD, to, f"Re: {subject}", reply)
            
        elif action[0] == "meeting":
            _, to, subject = action
            print(f"Sending meeting response to {to}")
            reply = f"""Hi,

Regarding the meeting request: "{subject}"

I confirm my interest and availability. Please let me know the finalized time and any preparation required.

Best regards,
Blesson
"""
            send_reply(EMAIL, PASSWORD, to, f"Re: {subject}", reply)

        else:  # generic
            _, to, subject = action
            print(f"Sending generic reply to {to}")
            reply = f"""Hi,

This is an automated response regarding: "{subject}".

I've received your message and will respond shortly.

Regards,  
Blesson
"""
            send_reply(EMAIL, PASSWORD, to, f"Re: {subject}", reply)

    print(f"\nAI agent finished processing. Found {essential_count} essential emails out of {len(emails)}.")

if __name__ == "__main__":
    run_agent()