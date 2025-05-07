import smtplib
from email.message import EmailMessage

def send_reply(email_user, email_pass, to_address, subject, message_body):
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = email_user
        msg["To"] = to_address
        msg.set_content(message_body)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(email_user, email_pass)
            server.send_message(msg)
        print(f"Reply sent to {to_address}")
    except Exception as e:
        print(f"Failed to send reply to {to_address}: {e}")
