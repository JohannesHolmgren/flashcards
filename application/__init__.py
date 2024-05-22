"""
    
    This file contains the the application creator.

    It's important that the name is '__init__.py' to
    tell python that the directory 'app' is a package.

"""
import os
from flask import Flask

# The app creator
def create_app(test_config=None):
    # Create app and set config files relative to instance (main) folder
    app = Flask(__name__, instance_relative_config=True)
    
    # Set a temporary secret key which should be overridden later
    # Set path to database for app
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE = os.path.join(app.instance_path, 'app.sqlite')
    )

    if test_config is None:
        # Load configurations from config if not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed
        app.config.from_mapping(test_config)
    
    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # A simple start page
    @app.route('/')
    def home():
        return 'HOME PAGE'
    
    return app