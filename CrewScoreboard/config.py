import os
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    """
    ============================[ Database configuration ]===========================    
    Examples:
    postgresql://postgres:my_password@localhost:5432/my_database
    sqlite:///:memory: 
    sqlite:///my_database.db
    mysql://user:passwd@ip:port/my_db
    """

    SQLALCHEMY_DATABASE_URI = 'sqlite:///debug.db'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    """
    ============================[ Development configuration ]========================    
    DO NOT LEAVE DEBUG SET TO TRUE IN PRODUCTION!
    IT WILL ENABLE ARBITRARY CODE EXECUTION!
    """
    # Various application settings
    DEBUG = False

    """
    ============================[ Security configuration ]===========================    
    Yeah this stuff is probably important
    """

    SECRET_KEY = 'Youll-never-guess-this'

    # Flask-Security config
    SECURITY_URL_PREFIX = "/admin"
    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    SECURITY_PASSWORD_SALT = 'thisIsPossiblyAGoodSaltIDontReallyKnowThoughButItProbablyWontHurt'

    # Flask-Security URLs, overridden because they don't put a / at the end
    SECURITY_LOGIN_URL = "/login/"
    SECURITY_LOGOUT_URL = "/logout/"
    SECURITY_REGISTER_URL = "/register/"

    SECURITY_POST_LOGIN_VIEW = "/admin/"
    SECURITY_POST_LOGOUT_VIEW = "/admin/"
    SECURITY_POST_REGISTER_VIEW = "/admin/"

    # Flask-Security features
    SECURITY_REGISTERABLE = False
    SECURITY_SEND_REGISTER_EMAIL = False

    """
    ============================[ Logging configuration ]============================
    Logging be good, logging be great.
    Gotta love logging.
    """
    # By default, we use a rotating log.
    # Each backup has a max size of 5 KB, and 5 coppies are kept
    # (Named like app.log.1, app.log.2, etc...    

    LOG_FILE_LOCATION = 'CrewScoreboard.log'
    LOG_FILE_SIZE_LIMIT_BYTES = 5000
    LOG_FILE_NUM_BACKUPS = 5

    """
    ============================[ Email configuration ]============================
    Emails can be sent in the event of an error.
    This only applies while NOT running in debug mode.
    """

    ALERTS_MAIL_ENABLED = False
    ALERTS_MAIL_SERVER = '127.0.0.1'
    ALERTS_MAIL_ORIGIN = 'error@example.com'
    ALERTS_ADMIN_EMAILS = ['UhOh@example.com', 'OhNo@example.com']

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.db')

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.db')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
