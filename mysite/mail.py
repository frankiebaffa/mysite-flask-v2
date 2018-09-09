import local_settings

def MailConfig(app):
    # configure the settings for flask_mail
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USE_SSL"] = True
    app.config["MAIL_USERNAME"] = 'frankiebaffa.com@gmail.com'

    # Define the password within a local file 'local_settings.py' as:
    #       MAIL_PASSWORD = 'password-of-your-choice'
    app.config["MAIL_PASSWORD"] = local_settings.MAIL_PASSWORD

