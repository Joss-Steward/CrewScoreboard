import datetime

from peewee import *
from flask.ext.security import Security, PeeweeUserDatastore, UserMixin, RoleMixin, login_required, current_user

from flask_admin.contrib.peewee import ModelView

from CrewScoreboard import app

class BaseModel(Model):
    class Meta:
        database = app.db

class Team(BaseModel):
    name = CharField()
    points = IntegerField()
    team_color = CharField()

class Student(BaseModel):
    name = TextField()
    team = ForeignKeyField(Team, related_name='students')

class Role(BaseModel, RoleMixin):
    name = CharField(unique=True)
    description = TextField(null=True)

class User(BaseModel, UserMixin):
    email = TextField()
    password = TextField()
    active = BooleanField(default=True)
    confirmed_at = DateTimeField(null=True)

class UserRoles(BaseModel):
    # Because peewee does not come with built-in many-to-many
    # relationships, we need this intermediary class to link
    # user to roles.
    user = ForeignKeyField(User, related_name='roles')
    role = ForeignKeyField(Role, related_name='users')
    name = property(lambda self: self.role.name)
    description = property(lambda self: self.role.description)

class SecureModelView(ModelView):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):        
        # Override builtin _handle_view in order to redirect users when a view is not accessible.
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))

class UserAdminView(SecureModelView):
    column_exclude_list = ['confirmed_at']

def create_tables():
    app.db.connect()
    app.db.create_tables([Team, Student, Role, User, UserRoles])

