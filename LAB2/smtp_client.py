import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure logging
logging.basicConfig(
    filename="email_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Replace with your Ethereal credentials
SMTP_SERVER = "smtp.ethereal.email"
SMTP_PORT = 587
USERNAME = ""
PASSWORD = ""

def send_email():
    sender = USERNAME
    receiver = "receiver@example.com"   # can be anything, will show in dashboard

    # Create the email
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = "Test Email from Python"

    body = "Hello! This is a test email sent using Ethereal Email (no phone needed)."
    msg.attach(MIMEText(body, "plain"))

    try:
        logging.info("Connecting to SMTP server...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        
        logging.info("Starting TLS encryption...")
        server.starttls()
        
        logging.info("Logging in...")
        server.login(USERNAME, PASSWORD)
        
        logging.info("Sending email...")
        server.sendmail(sender, receiver, msg.as_string())
        
        logging.info("Closing connection...")
        server.quit()
        
        print("Email sent! Check Ethereal dashboard.")
        logging.info("Email sent successfully!")
    except Exception as e:
        print("Error:", e)
        logging.error(f"Error occurred: {e}")

send_email()
