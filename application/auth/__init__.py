from flask_login import LoginManager
from .loginform import LoginForm
from .registrationform import RegistrationForm
from application.models.user import User

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

# Specify for login manager function to retrieve user from user_id
@login_manager.user_loader
def loader_user(user_id: int):
    return User.query.get(int(user_id))

def init_app(app):
    login_manager.init_app(app)

