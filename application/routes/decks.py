from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from application.models import Deckhandler, Userhandler

# Create blueprint for deck views
bp = Blueprint('decks', __name__)

# A simple start page
@bp.route('/')
def home():
    return redirect(url_for('decks.index'))

@bp.route('/decks', methods=('GET', 'POST'))
def index():
    test_user = Userhandler.get_test_user()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        Deckhandler.add_deck(name, description, test_user)

    decks = Deckhandler.get_decks(test_user)
    return render_template('decks/index.html', decks=decks)
