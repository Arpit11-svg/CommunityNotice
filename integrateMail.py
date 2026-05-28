from dotenv import load_dotenv
import os
from flask_mail import Mail

load_dotenv()

mail = Mail()

def configure_mail(app):

    # Flask-Mail configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    # Environment variables
    app.config['MAIL_USERNAME'] = os.getenv("GMAIL_USER")
    app.config['MAIL_PASSWORD'] = os.getenv("GMAIL_PASSWORD")

    # Initialize mail
    mail.init_app(app)