import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from api.models.patient_model import Patient
import os

class EmailSender:
    def send_notification(self, patient: Patient, message: str):
        print("Sending email...")
        try:
            sender_email = os.getenv('EMAIL_USER')
            app_password = os.getenv('EMAIL_PASSWORD')
            msg = MIMEMultipart()
            msg['From'] = os.getenv('EMAIL_USER')
            msg['To'] = patient.email_address
            msg['Subject'] = "New patient"
            msg.attach(MIMEText(message, 'plain'))

            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, app_password)
                server.sendmail(sender_email, patient.email_address, msg.as_string())

            print("Email sent successfully!")

        except Exception as e:
            print(f"Failed to send email: {e}")