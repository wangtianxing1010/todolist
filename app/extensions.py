from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

import app
from flask import request, current_app
from flask_babel import Babel, lazy_gettext as _l

db = SQLAlchemy()
csrf = CSRFProtect()
babel = Babel()
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = _l("Please login to access this page")


@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))


@babel.localeselector
def get_locale():
    if current_user.is_authenticated and current_user.locale is not None:
        return current_user.locale

    locale = request.cookies.get('locale')
    if locale is not None:
        return locale
    return request.accept_languages.best_match(current_app.config['TODOLIST_LOCALES'])