import os

from flask_script import Server, Manager, Command, prompt_bool, prompt, prompt_pass
from flask_migrate import Migrate, MigrateCommand
from CrewScoreboard import create_app, db

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

# This provides most of the database setup logic and such
manager.add_command('db', MigrateCommand)

#@manager.option('-u', '--username', dest='username', default=None)
#@manager.option('-p', '--password', dest='password', default=None)
@manager.command
def admin(username=None, password=None):
    "Create a new admin user, with the supplied username and password"

    while username is None:
        username = prompt('Please enter a Username (preferably an email)')

    while password is None:
        password = prompt_pass('Please enter a Password')
    
    auth.create_admin(username, password)

if __name__ == "__main__":
    try:
        manager.run()
    except KeyboardInterrupt:
        print("Ended by Ctrl-C")
        