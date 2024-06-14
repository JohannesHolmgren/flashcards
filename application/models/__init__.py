from flask_sqlalchemy import SQLAlchemy

from .base import db
from .deckhandler import Deckhandler
from .cardhandler import Cardhandler
from .userhandler import Userhandler

def init_app(app): 
    db.init_app(app)
    
    # Create tables
    with app.app_context():
        db.create_all()

