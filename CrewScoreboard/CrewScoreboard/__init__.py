from flask import Flask
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from CrewScoreboard.logging import configure_logging

#bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    configure_logging(app)

    app.logger.info("Application Startup")

    if app.debug:
        app.logger.warning("APPLICATION STARTED IN DEBUG MODE. ARBITRARY CODE EXECUTION WILL BE POSSIBLE.")

    #bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    app.logger.debug("Adding 'main' blueprint")
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    app.logger.debug("Adding 'auth' blueprint")
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    app.logger.debug("Adding 'admin' blueprint")
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    app.logger.info("Application created successfully")
    return app
