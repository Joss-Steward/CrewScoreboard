"""
The flask application package.
"""

from flask import Flask
from playhouse.db_url import connect
from flask.ext.security import Security, PeeweeUserDatastore, UserMixin, RoleMixin, login_required

#from peewee import
import logging 

# Load the application configuration first from the default file, then override
# it with the settings in the file specified in the environmental variable
# (if one is given).
app = Flask(__name__)
app.config.from_object('CrewScoreboard.default_settings')

# If no settings file was set, catch the error and log it, but continue.
# (This should happen when debugging. If it happens in prod, you haven't 
#  set up the config file properly).
try:
    app.config.from_envvar('CREWSCOREBOARD_SETTINGS')
except RuntimeError as e:
    print('DANGER')
    print('No configuration file was set in the environmental variables')
    print('Falling back to default configuration')    

import CrewScoreboard.error_handling

# Set up the database
app.db = connect(app.config['DATABASE'])

import CrewScoreboard.models

# Setup Flask-Security
user_datastore = PeeweeUserDatastore(app.db, models.User, models.Role, models.UserRoles)
security = Security(app, user_datastore)

import CrewScoreboard.views