import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(to_email, subject, body):
    sender_email = os.environ.get('MAIL_USERNAME', 'adar04954@gmail.com')
    sender_password = os.environ.get('MAIL_PASSWORD', 'ehrf ajby ukoo djsj')

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)
        server.quit()
        print(f"📤 אימייל נשלח ל- {to_email}")
        return True
    except Exception as e:
        print(f"❌ שגיאה בשליחת אימייל: {e}")
        return False
