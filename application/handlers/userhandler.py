from application.models.base import db
from application.models.user import User
from config import Config

class Userhandler:

    @staticmethod
    def get_test_user():
        test_user = User.query.filter_by(username='testuser').first()
        if test_user:
            return test_user
        user = User()
        user.username = Config.TEST_USERNAME
        user.email = Config.TEST_EMAIL
        user.set_password(Config.TEST_PASSWORD)
        db.session.add(user)
        db.session.commit()
        return user