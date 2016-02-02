import datetime

from peewee import *
from CrewScoreboard import app
from flask.ext.security import RoleMixin, UserMixin

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

def create_tables():
    app.db.connect()
    app.db.create_tables([Team, Student, Role, User, UserRoles])
    app.user_datastore.create_role(name='user')
    app.user_datastore.create_role(name='admin')
    app.db.commit()
    app.db.close()

def drop_tables():
    app.db.connect()
    app.db.drop_tables([Team, Student, Role, User, UserRoles])
    app.db.commit()
    app.db.close()