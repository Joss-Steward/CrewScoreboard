from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView
from flask.ext.security import Security, PeeweeUserDatastore, login_required, current_user

from CrewScoreboard import app, models

class SecureModelView(ModelView):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('admin'):
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
    column_exclude_list = ['password, confirmed_at']

# Setup Flask-Admin
admin = Admin(app, name='Crew Scoreboard', template_mode='bootstrap3')
admin.add_view(UserAdminView(model=models.User, endpoint='model_view_user', name='Users'))