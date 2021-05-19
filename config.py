import os
#need to learn how to use the config.py setup
class Config(object):
    TECHNICAL_USER=os.environ.get('TECHNICAL_USER')
    SECRET_KEY=os.environ.get('SECRET_KEY')