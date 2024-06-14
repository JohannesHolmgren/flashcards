import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    TEST_USERNAME = os.getenv('TEST_USERNAME')
    TEST_EMAIL = os.getenv('TEST_EMAIL')
    TEST_PASSWORD = os.getenv('TEST_PASSWORD')