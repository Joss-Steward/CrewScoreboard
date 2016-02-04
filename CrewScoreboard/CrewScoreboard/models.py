import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import db, login_manager

class Permission:
    ADD_POINTS =     0b00000001
    REMOVE_POINTS =  0b00000010
    ADD_USERS =      0b00000100
    REMOVE_USERS =   0b00001000
    ADD_TEAMS =      0b00010000
    REMOVE_TEAMS =   0b00100000

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    def __repr__(self):
        return '<Role %r>' % self.name

    @staticmethod
    def insert_roles():
        roles = {
            'Team_Leader': (Permission.ADD_POINTS | Permission.REMOVE_POINTS, True),
            'Administrator': (  Permission.ADD_POINTS | 
                                Permission.REMOVE_POINTS | 
                                Permission.ADD_USERS |
                                Permission.REMOVE_USERS |
                                Permission.ADD_TEAMS |
                                Permission.REMOVE_TEAMS, True)
        }

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

user_teams_table = Table('user_teams_table', db.Model.metadata,
    Column('user_id', Integer, ForeignKey('teams.id')),
    Column('team_id', Integer, ForeignKey('siteusers.id'))
)

class User(UserMixin, db.Model):
    __tablename__ = 'siteusers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

    teams = relationship(
        "Team",
        secondary=user_teams_table,
        back_populates="users")

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

class AnonymouseUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

login_manager.anonymous_user = AnonymouseUser

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    points = db.relationship('Point', backref='team', lazy='dynamic')
    users = relationship(
        "User",
        secondary=user_teams_table,
        back_populates="teams")

class Point(db.Model):
    __tablename__ = 'points'
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    value = db.Column(db.Numeric)
    header = db.Column(db.Text())
    body = db.Column(db.Text())

# Other functions....
def create_admin(username, password):
    user = User.query.filter_by(username=username).first()
    if user is None:
        user = User()
    else:
        print("User (" + username + ") already exists. Altering password and adding permissions.")
    user.username = username
    user.password = password
    role = Role.query.filter_by(name='Administrator').first()
    if role is None:
        print("Failed to add admin user because the Administrator role does not exist.")
        print("Please boostrap the database first, then try again.")
        exit(1)
    user.role = role
    db.session.add(user)
    db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))