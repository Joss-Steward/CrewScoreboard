import os

from flask_script import Server, Manager, Command, Shell, prompt, prompt_pass, prompt_bool
from flask_migrate import Migrate, MigrateCommand
from CrewScoreboard import create_app, db
from CrewScoreboard.models import User, Role, create_admin

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

# This provides most of the database setup logic and such
manager.add_command('db', MigrateCommand)

# Do a little setup before creating the interactive shell
def make_shell_context():
    app.logger.info("Interactive shell session started from manage.py")
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))

#@manager.option('-u', '--username', dest='username', default=None)
#@manager.option('-p', '--password', dest='password', default=None)
@manager.command
def admin(username=None, password=None):
    "Create a new admin user, with the supplied username and password"

    while username is None:
        username = prompt('Please enter a Username (preferably an email)')

    while password is None:
        password = prompt_pass('Please enter a Password')

    try:    
        create_admin(username, password)
        app.logger.info("Added a new admin user (" + username + ") from manage.py")
    except:
        print("Something went wrong, sorry.")

if __name__ == "__main__":
    try:        
        manager.run()
    except KeyboardInterrupt:
        print("Ended by Ctrl-C")
        