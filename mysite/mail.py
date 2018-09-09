import local_settings

def MailConfig(app):
    # configure the settings for flask_mail
    # set variable CONTACT_EMAIL as local_settings.CONTACT_EMAIL
    app.config['CONTACT_EMAIL'] = local_settings.CONTACT_EMAIL
    app.config["MAIL_SERVER"] = local_settings.MAIL_SERVER
    app.config["MAIL_PORT"] = local_settings.MAIL_PORT
    app.config["MAIL_USE_SSL"] = local_settings.MAIL_USE_SSL
    app.config["MAIL_USERNAME"] = local_settings.MAIL_USERNAME

    # Define the password within a local file 'local_settings.py' as:
    #       MAIL_PASSWORD = 'password-of-your-choice'
    app.config["MAIL_PASSWORD"] = local_settings.MAIL_PASSWORD

