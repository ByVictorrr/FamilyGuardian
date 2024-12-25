import smtplib
from email.mime.text import MIMEText

def send_alert(recipient_email, snapshot_path):
    sender_email = "your_email@gmail.com"
    password = "your_email_password"

    # Email content
    subject = "Alert: Unrecognized Face Detected"
    body = "An unfamiliar face was detected. Check the attached snapshot."
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    # Send email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

    print(f"Alert sent to {recipient_email}")

send_alert("recipient_email@example.com", "snapshot.jpg")
