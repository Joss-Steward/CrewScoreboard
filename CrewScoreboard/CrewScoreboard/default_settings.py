"""
This is the default configuration file.
It is provided as a sample.
For production, you should not run this app with a SQLite database.
You should not run this app in debug mode unless you are actually debugging.
"""

# The database configuration
DATABASE = {
    'name': 'debug.db',
    'engine': 'peewee.SqliteDatabase',
}

# Various application settings
#DEBUG = True

"""
============================[ Logging configuration ]============================
Logging be good, logging be great.
Gotta love logging.
"""

# Log File Configurations
"""
By default, we use a rotating log.
Each backup has a max size of 5 KB, and 5 coppies are kept
(Named like app.log.1, app.log.2, etc...
"""

LOG_FILE_LOCATION = 'CrewScoreboard.log'
LOG_FILE_SIZE_LIMIT_BYTES = 5000
LOG_FILE_NUM_BACKUPS = 5

# Email Alert Configurations
"""
Emails can be sent in the event of an error.
This only applies while NOT running in debug mode.
"""

ALERTS_MAIL_SERVER = '127.0.0.1'
ALERTS_MAIL_ORIGIN = 'error@example.com'
ALERTS_ADMIN_EMAILS = ['UhOh@example.com', 'OhNo@example.com']
