from flask_login import LoginManager
from .loginform import LoginForm
from .registrationform import RegistrationForm

login_manager = LoginManager()

def init_app(app):
    login_manager.init_app(app)