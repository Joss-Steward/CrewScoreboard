from flask.ext.security import Security, PeeweeUserDatastore, UserMixin, RoleMixin, login_required
from flask.ext.security.utils import encrypt_password
from CrewScoreboard import app, models

# Setup Flask-Security
app.user_datastore = PeeweeUserDatastore(app.db, models.User, models.Role, models.UserRoles)
app.security = Security(app, app.user_datastore)

def create_admin(email, password):
    role = app.user_datastore.find_role('admin')
    app.user_datastore.create_user(
        email=email, 
        password=encrypt_password(password), 
        roles=[role]
    )