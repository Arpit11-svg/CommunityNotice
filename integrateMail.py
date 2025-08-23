import json
from flask_mail import Mail

mail = Mail()

def configure_mail(app):    #we pass 'app' as an argument in function/method definition
    # Load your JSON parameters
    with open('config.json', 'r') as f:
        parameter = json.load(f)['parameter']

    # Set up Flask-Mail configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = parameter['gmail-user']
    app.config['MAIL_PASSWORD'] = parameter['gmail-password']

    # Initialize mail with Flask app
    mail.init_app(app)

