from flask_mail import Mail, Message
import os

mail = Mail()

def init_mail(app):
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')  # your@gmail.com
    app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')  # Gmail App Password
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('EMAIL_USER')
    mail.init_app(app)

def send_email_notification(subject, body):
    recipient = os.environ.get('EMAIL_TO')
    if not recipient:
        print("❌ EMAIL_TO is not set in environment variables.")
        return

    try:
        msg = Message(subject=subject, recipients=[recipient])
        msg.body = body
        mail.send(msg)
        print(f"✅ Email sent to {recipient}")
    except Exception as e:
        print(f"❌ Email sending failed: {e}")
