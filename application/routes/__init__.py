from .card_editor import bp as card_editor_bp
from .play import bp as play_bp

def init_app(app):
    app.register_blueprint(card_editor_bp)
    app.register_blueprint(play_bp)

