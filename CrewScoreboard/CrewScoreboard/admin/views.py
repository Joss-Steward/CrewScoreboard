from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required
from ..decorators import permission_required
from ..models import Permission, User, Role
from . import admin
from .forms import AddUserForm, EditUserForm
from .. import db

@admin.route('/')
@login_required
@permission_required(Permission.ADD_USERS)
def admin_dashboard():
    return render_template('admin/admin_dashboard.html')

# I would really like to use PUT for adding new users,
# but apparently modern browsers don't support PUT.
@admin.route('/user', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ADD_USERS | Permission.REMOVE_USERS)
def manage_users(user_id=None):
    users = db.session.query(User).all()
    form = AddUserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is not None:
                flash('User (' + form.username.data + ') already exists.')
                form.password.data = ''
                return render_template('admin/manage_users.html', form=form, users=users)        
            user = User()
            user.username = form.username.data
            user.password = form.password.data
            role = Role.query.filter_by(name='Team_Leader').first()
            user.role = role
            db.session.add(user)
            db.session.commit()
            flash('User added successfully', 'success')
            return redirect(url_for('admin.manage_users'))
        flash('Response not validated')
    else:
        return render_template('admin/manage_users.html', form=form, users=users)

@admin.route('/user/<user_id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ADD_USERS | Permission.REMOVE_USERS)
def edit_user(user_id):
    form = EditUserForm()
    print(form.errors)
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        flash('User not found')
        return redirect(url_for('admin.manage_users'))

    form.username.data = user.username
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.password.data is not None: 
                if form.password.data != '':     
                    user.password = form.password.data
                    flash('Password successfully changed')
            
            user.username = form.username.data
            db.session.merge(user)
            db.session.commit()
            flash('Changes successfully saved')
        else:
            flash('Response not validated')

    return render_template('admin/edit_user.html', form=form, user=user)