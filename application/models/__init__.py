from flask_sqlalchemy import SQLAlchemy
from .base import db

def init_app(app): 
    # TODO move these to main __init__.py
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SECRET_KEY'] = 'dev'
    # Init database
    db.init_app(app)
    
    