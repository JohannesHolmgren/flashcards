from .generate_deck import bp as generate_deck_bp
from .card_editor import bp as card_editor_bp
from .deck_editor import bp as deck_editor_bp
from .go_back import bp as go_back_bp
from .decks import bp as decks_bp
from .play import bp as play_bp
from .auth import bp as auth_bp

def init_app(app):
    app.register_blueprint(generate_deck_bp)
    app.register_blueprint(card_editor_bp)
    app.register_blueprint(deck_editor_bp)
    app.register_blueprint(go_back_bp)
    app.register_blueprint(decks_bp)
    app.register_blueprint(play_bp)
    app.register_blueprint(auth_bp)


