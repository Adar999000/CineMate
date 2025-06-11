import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_email, subject, body):
    sender_email = "adar04954@gmail.com"
    sender_password = "ehrf ajby ukoo djsj"  # סיסמת אפליקציה

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
    except Exception as e:
        print(f"❌ שגיאה בשליחת מייל: {e}")
