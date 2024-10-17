from flask import Flask
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_login import LoginManager


from config import Config
from app.extensions import db
from app.main import bp as main_bp
from app.accounts import bp as accounts_bp
from app.events import bp as events_bp
from app.models.accounts import User


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    csrf = CSRFProtect(app)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'accounts.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(main_bp)

    app.register_blueprint(accounts_bp, url_prefix='/accounts')

    app.register_blueprint(events_bp, url_prefix='/events')

    return app
