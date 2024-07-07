from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_login import login_required, current_user

from application.handlers import Deckhandler
from application.routes.page_stack import PageStack

# Create blueprint for deck views
bp = Blueprint('decks', __name__)

# A simple start page
@PageStack.stack_page
@bp.route('/')
def home():
    return redirect(url_for('decks.index'))

@PageStack.stack_page
@bp.route('/decks', methods=('GET', 'POST'))
@login_required
def index():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        Deckhandler.add_deck(name, description, current_user)

    decks = Deckhandler.get_decks(current_user)
    return render_template('decks/index.html', decks=decks)
