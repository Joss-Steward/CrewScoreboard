from flask import render_template
from flask_login import login_required
from ..decorators import permission_required
from ..models import Permission
from . import admin

@admin.route('/')
@login_required
@permission_required(Permission.ADD_USERS)
def admin_dashboard():
    return render_template('admin_dashboard.html')
