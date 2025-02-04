from flask_mail import Mail, Message
from flask import Flask
from config.config import Config 

MAIL_SERVER = Config.MAIL_SERVER
MAIL_PORT = Config.MAIL_PORT
MAIL_USERNAME = Config.MAIL_USERNAME
MAIL_PASSWORD = Config.MAIL_PASSWORD
MAIL_USE_TLS = Config.MAIL_USE_TLS
MAIL_USE_SSL = Config.MAIL_USE_SSL

app = Flask(__name__)

# Configuración de Flask-Mail
app.config["MAIL_SERVER"] = MAIL_SERVER
app.config["MAIL_PORT"] = MAIL_PORT
app.config["MAIL_USERNAME"] = MAIL_USERNAME
app.config["MAIL_PASSWORD"] = MAIL_PASSWORD
app.config["MAIL_USE_TLS"] = MAIL_USE_TLS
app.config["MAIL_USE_SSL"] = MAIL_USE_SSL

mail = Mail(app)

def send_email(recipient, subject, body):
    """
    Sent a mail of notification.
    """
    try:
        msg = Message(subject=subject,
                      sender=MAIL_USERNAME,
                      recipients=[recipient])
        msg.body = body
        with app.app_context():
            mail.send(msg)
        return True
    except Exception as e:
        print(f"Error to sent mail.: {e}")
        return False