class BaseConfig(object):
    SECRET_KEY = 'abcdef123456'
    DEBUG = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True