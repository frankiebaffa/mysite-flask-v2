# get os
import os
import local_settings

# set variable basedir as location of this file
basedir = os.path.abspath(os.path.dirname(__file__))

# create object Config for application configuration
class Config(object):
    # create variable SECRET_KEY as environment SECRET_KEY
    SECRET_KEY = local_settings.SECRET_KEY
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# only run app if
if __name__ == '__main__':
    app.run()
