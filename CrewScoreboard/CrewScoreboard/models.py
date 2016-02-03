import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager

class Permission:
    ADD_POINTS = 0x01
    ADD_USERS = 0x02    

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
            'Team_Leader': (Permission.ADD_POINTS, True),
            'Administrator': (Permission.ADD_POINTS | Permission.ADD_USERS, True)
        }

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

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

def create_admin(email, password):
    user = User.query.filter_by(username=email).first()
    if user is None:
        user = User()
    else:
        print("User (" + email + ") already exists. Altering password and adding permissions.")
    user.email = email
    user.username = email
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