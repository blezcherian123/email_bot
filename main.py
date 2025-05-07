from email_reader import get_emails
from email_sender import send_reply

# Replace these with your actual Gmail and app password
EMAIL = "blessoncbiju123@gmail.com"
PASSWORD = "cmbdugbtujkhewpi"

# Step 1: Get essential emails
emails = get_emails(EMAIL, PASSWORD)

# Step 2: Send replies
for mail in emails:
    sender = mail["from"]
    subject = mail["subject"]
    body = mail["body"]

    print(f"Replying to: {sender}")
    reply_message = f"""Hi,

This is an automated reply to your email regarding: "{subject}".

Thank you for reaching out. We have received your message and will get back to you shortly.

Best regards,  
Your Email Bot
"""
    send_reply(EMAIL, PASSWORD, sender, f"Re: {subject}", reply_message)

print("All replies sent.")
