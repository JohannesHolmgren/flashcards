"""
    
    This file contains the the application creator.

    It's important that the name is '__init__.py' to
    tell python that the directory 'app' is a package.

"""
from flask import Flask

from . import models
from . import routes
from . import handlers

# The app creator
def create_app(config_class='config.Config'):
    # Create app
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Init the database
    models.init_app(app)
    
    # Init routes
    routes.init_app(app)

    # Init handlers
    handlers.init_app(app)

    return app