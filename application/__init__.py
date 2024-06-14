"""
    
    This file contains the the application creator.

    It's important that the name is '__init__.py' to
    tell python that the directory 'app' is a package.

"""
from flask import Flask

from . import decks
from . import models
from . import routes

# The app creator
def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Init the database
    models.init_app(app)

    # Init routes
    routes.init_app(app)

    # Register blueprint for deck-view
    app.register_blueprint(decks.bp)

    return app