import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# ================= SINGLE EMAIL =================
def send_email(receiver_email, subject, body):
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print(f"Email sent to {receiver_email}")
    except Exception as e:
        print(f"Error: {e}")


# ================= BULK EMAIL =================
def send_bulk_emails(file_path, sender_email, sender_password):
    data = pd.read_excel(file_path)   # ✅ FIXED

    for index, row in data.iterrows():
        receiver_email = row['email']
        name = row['name']
        message = row.get('message', 'No message provided')

        subject = "Automated Notification System"

        body = f"""Hello {name}"""

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            print(f"Email sent to {receiver_email}")
        except Exception as e:
            print(f"Failed: {e}")