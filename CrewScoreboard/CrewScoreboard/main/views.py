from flask import render_template
from flask_login import login_required
from ..decorators import permission_required
from ..models import Permission
from . import main

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/admin')
@login_required
@permission_required(Permission.ADD_USERS)
def amin():
    return "Admins only"