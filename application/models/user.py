from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .base import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    signup_date = db.Column(db.DateTime, default=datetime.now(datetime.UTC))
    decks = db.relationship('Deck', backref='owner', lazy=True)

    def __repr__(self):
        return f'<User {self.id}, {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)