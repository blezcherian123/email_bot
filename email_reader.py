import imaplib
import email
from email.header import decode_header

def get_emails(email_user, email_pass):
    print("\n📬 Starting email check...")
    
    # Connect to Gmail
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(email_user, email_pass)
    mail.select("inbox")

    # Get emails
    status, messages = mail.search(None, "ALL")
    email_ids = messages[0].split()
    emails = []

    for num in email_ids[-10:]:  # Last 10 emails
        status, msg_data = mail.fetch(num, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                
                # Get basic email info
                try:
                    subject, encoding = decode_header(msg["Subject"])[0]
                    subject = subject.decode(encoding or "utf-8") if isinstance(subject, bytes) else subject
                    from_ = msg.get("From", "Unknown Sender")
                except:
                    subject = "No Subject"
                    from_ = "Unknown Sender"

                # Get body
                body = extract_email_body(msg)

                emails.append({
                    "from": from_,
                    "subject": subject,
                    "body": body
                })
                
                # Simple status output
                if any(keyword in subject.lower() for keyword in ['urgent', 'important', 'action required']):
                    print(f"❗ Urgent: {subject}")
                else:
                    print(f"📩 Checking: {subject}")

    mail.logout()
    print("\n✅ Email check complete\n")
    return emails

def extract_email_body(msg):
    """Helper function to extract email body with better error handling"""
    body = ""
    try:
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain" and "attachment" not in str(part.get("Content-Disposition", "")):
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode()
    except:
        body = "[Email content could not be read]"
    return body
