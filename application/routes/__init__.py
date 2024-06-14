from .card_editor import bp as card_editor_bp

def init_app(app):
    app.register_blueprint(card_editor_bp)