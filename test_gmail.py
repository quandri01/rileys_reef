import os
import smtplib
from dotenv import load_dotenv

load_dotenv()

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_PASS")
TO_EMAIL = GMAIL_USER  # Send to yourself for testing

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(GMAIL_USER, GMAIL_PASS)
        server.sendmail(GMAIL_USER, TO_EMAIL, "Subject: Test Email\n\nThis is a test email.")
        print("✅ Email sent successfully!")
except Exception as e:
    print("❌ Error sending email:", e)
