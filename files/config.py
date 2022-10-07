class Config(object):
    DEBUG = True
    SECRET_HERE = '249y823r9v8238r9u'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secret-key'
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    BABEL_DEFAULT_LOCALE = 'en_US'
    LANGUAGES = ['en', 'ru']
