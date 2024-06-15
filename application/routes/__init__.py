from .card_editor import bp as card_editor_bp
from .play import bp as play_bp
from .deck_editor import bp as deck_editor_bp

def init_app(app):
    app.register_blueprint(card_editor_bp)
    app.register_blueprint(play_bp)
    app.register_blueprint(deck_editor_bp)

