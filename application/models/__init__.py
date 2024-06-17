from flask_sqlalchemy import SQLAlchemy

from .base import db

def init_app(app): 
    db.init_app(app)
    
    # Create tables
    with app.app_context():
        db.create_all()

