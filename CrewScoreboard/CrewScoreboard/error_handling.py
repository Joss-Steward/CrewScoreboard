"""
This file configures logging and other application error handling traits.
When running in Debug mode, no email alerts will be sent.
"""

from CrewScoreboard import app  
import logging
from logging import Formatter, getLogger
from logging.handlers import RotatingFileHandler

# Configure the file logging and enable email alerts if in production
file_handler = RotatingFileHandler(app.config['LOG_FILE_LOCATION'], 
                                    maxBytes = app.config['LOG_FILE_SIZE_LIMIT_BYTES'], 
                                    backupCount = app.config['LOG_FILE_NUM_BACKUPS'])

file_handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))

loggers = [getLogger('peewee')]


if not app.debug:
    from logging.handlers import SMTPHandler
    mail_handler = SMTPHandler(app.config['ALERTS_MAIL_SERVER'], 
                                app.config['ALERTS_MAIL_ORIGIN'], 
                                app.config['ALERTS_ADMIN_EMAILS'], 
                                'Application Error')
    mail_handler.setFormatter(Formatter('''
    Message type:       %(levelname)s
    Location:           %(pathname)s:%(lineno)d
    Module:             %(module)s
    Function:           %(funcName)s
    Time:               %(asctime)s

    Message:

    %(message)s
    '''))
    app.logger.addHandler(mail_handler)
    for logger in loggers:
        logger.addHandler(mail_handler)
    file_handler.setLevel(logging.WARNING)
else:
    file_handler.setLevel(logging.INFO)

app.logger.addHandler(file_handler)

for logger in loggers:
    logger.addHandler(file_handler)