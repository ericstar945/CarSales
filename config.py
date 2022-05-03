import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\xcbD\xee\xa6\xd9\x9cLcy\xe0\x0c.\x03\xcd%\x9d'

    MONGODB_SETTINGS = { 'db': 'CarDB' }