from flask.ext.script import Server, Manager, Command, prompt_bool, prompt, prompt_pass
from CrewScoreboard import app, models, auth

manager = Manager(app)

# commands:
# reset_db
# add_admin_user

@manager.command
def create():
    "Create the needed tables in the database. Will fail if the database already exists."
    print("Creating tables in database: " + app.config['DATABASE'])
    models.create_tables()
        
    try:
        print("Database created")
    except:
        print("Failed to create tables. Make sure the database is accessible and the tables don't already exist.")     
   
@manager.command
def drop(force=False):
    "Drop all of the tables in the database. THIS WILL DESTROY ALL OF YOUR DATA."

    print("Selected database: " + app.config['DATABASE'])
    print("WARNING: THIS WILL DESTROY ALL OF THE DATA FOR THIS WEBSITE")

    def drop_tables():
        try:
            models.drop_tables()
            print("Tables successfully dropped.")
        except:
            print("Failed to drop all tables. Make sure the database is accessible and the tables exist.")    
 
    if force:
        print("-f flag passed, dropping tables.")
        drop_tables()
    elif prompt_bool("Are you sure you want to drop the tables?"):
        drop_tables() 
  
@manager.command
def reset(force=False):
    "Drop and recreate all of this site's tables. THIS WILL DESTROY ALL OF YOUR DATA."

    print("Selected database: " + app.config['DATABASE'])
    print("WARNING: THIS WILL DESTROY ALL OF THE DATA FOR THIS WEBSITE")

    def drop_tables():
        try:
            models.drop_tables()
            print("Tables successfully dropped.")
        except:
            print("Failed to drop all tables. Make sure the database is accessible and the tables exist.")    
 
    if force:
        print("-f flag passed, dropping tables.")
        drop_tables()
    elif prompt_bool("Are you sure you want to drop the tables?"):
        drop_tables()   
    else:
        exit(1)

    print("Creating tables in database: " + app.config['DATABASE'])
        
    try:
        models.create_tables()
        print("Database created")
    except:
        print("Failed to create tables. Make sure the database is accessible and the tables don't already exist.")   

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
        