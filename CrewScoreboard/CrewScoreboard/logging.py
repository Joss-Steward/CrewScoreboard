"""
This file configures logging and other application error handling traits.
When running in Debug mode, no email alerts will be sent.
"""

import logging
from logging import Formatter, getLogger
from logging.handlers import RotatingFileHandler

# Custom log formatter, courtesy of 
# http://stackoverflow.com/questions/1343227/can-pythons-logging-format-be-modified-depending-on-the-message-log-level
class MyFormatter(logging.Formatter):
    FORMATS = {
        logging.CRITICAL :  logging._STYLES['{'][0]("{asctime}: CRITICAL : [{pathname} {lineno}] {message}"),
        logging.ERROR :     logging._STYLES['{'][0]("{asctime}: ERROR    : [{pathname} {lineno}] {message}"),        
        logging.WARNING :   logging._STYLES['{'][0]("{asctime}: WARNING  : [{module}] {message}"),
        logging.INFO :      logging._STYLES['{'][0]("{asctime}: INFO     : {message}"),
        logging.DEBUG :     logging._STYLES['{'][0]("{asctime}: DEBUG    : [{module} {lineno}] {message}"),
        'DEFAULT' :         logging._STYLES['{'][0]("{asctime}: NOTSET   : [{module} {lineno}] {message}")
    }

    def format(self, record):
        # Ugly. Should be better
        self._style = self.FORMATS.get(record.levelno, self.FORMATS['DEFAULT'])
        return logging.Formatter.format(self, record)

def configure_logging(app):
    master_formatter = MyFormatter()

    # Configure the file logging and enable email alerts if in production
    file_handler = RotatingFileHandler(
                        app.config['LOG_FILE_LOCATION'], 
                        maxBytes = app.config['LOG_FILE_SIZE_LIMIT_BYTES'], 
                        backupCount = app.config['LOG_FILE_NUM_BACKUPS']
                   )

    file_handler.setFormatter(master_formatter)

    if app.debug:
        # When I'm testing this, all of the log events are written to the console too
        # The format flask uses is annoying though, so I'm just going to change it to something I prefer
        for han in app.logger.handlers:
            han.setFormatter(master_formatter)

    loggers = [app.logger, logging.getLogger("sqlalchemy"), logging.getLogger('werkzeug')]

    error_handlers = [file_handler]

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
        
        mail_handler.setLever(logging.ERROR)
        file_handler.setLevel(logging.INFO)

        error_handlers.append(mail_handler)
    else:
        file_handler.setLevel(logging.DEBUG)

    for logger in loggers:
        logger.addHandler(file_handler)