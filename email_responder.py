import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_reply(to_email, subject, original_msg, from_email, app_password):
    reply_subject = f"RE: {subject}"
    reply_body = f"""Hi,\n\nThanks for your email regarding: "{subject}". We have noted the message:\n\n\"{original_msg}\"\n\nThis is an automated reply confirming receipt.\n\nRegards,\nEmail Bot"""

    # Compose the email
    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = reply_subject
    message.attach(MIMEText(reply_body, "plain"))

    try:
        # Connect to Gmail SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(from_email, app_password)
            server.send_message(message)
        print(f"Replied to {to_email} ✅")
    except Exception as e:
        print(f"Failed to send reply to {to_email}: {e}")
