import smtplib
from email.message import EmailMessage

def send_authentication_email(to_email, from_email, password):
    msg = EmailMessage()
    msg["Subject"] = "Authentication Required"
    msg["From"] = from_email
    msg["To"] = to_email
    msg.set_content("""Hello,

To proceed with your request, please answer the following authentication questions:

1. What is your full name?
2. What is your registered mobile number?
3. What are the last 4 digits of your account/card number?
4. What was your last transaction amount?

Thank you,
DBS Auto-Response Bot
""")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(from_email, password)
        smtp.send_message(msg)
