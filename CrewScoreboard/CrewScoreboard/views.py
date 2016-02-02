"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, Response
from CrewScoreboard import app, models, user_datastore, security
from flask.ext.security import Security, PeeweeUserDatastore, \
    UserMixin, RoleMixin, login_required
from flask.ext.security.utils import encrypt_password

#@app.route('/')
#@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    # Add a team just to test
    null_ptr = Team.create(name='Null Pointer', color='#00FF00', points=1000)
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )    


@app.before_first_request
def create_user():
    for Model in (models.Role, models.User, models.UserRoles):
        Model.drop_table(fail_silently=True)
        Model.create_table(fail_silently=True)
    user_datastore.create_user(email='matt@nobien.net', password=encrypt_password('password1'))

# Views
@app.route('/')
@login_required
def home():
    return render_template('index.html')