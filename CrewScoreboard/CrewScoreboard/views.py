"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, Response
from CrewScoreboard import app, models, auth
from flask.ext.security import Security, PeeweeUserDatastore, login_required

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

# Views
@app.route('/')
@login_required
def home():
    return render_template('index.html')