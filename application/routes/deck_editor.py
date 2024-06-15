"""
    This file contains all views for playing a deck.
"""

import random
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from application.models.cardhandler import Cardhandler
from application.models.deckhandler import Deckhandler
from application.models.userhandler import Userhandler

# Create blueprint for deck views
bp = Blueprint('deck_editor', __name__)

""" ---------- Routes ---------- """

@bp.route('/deck_editor/deck_delete/<int:deck_id>', methods=('GET', 'POST'))
def deck_delete(deck_id: int):
    Deckhandler.delete_deck(deck_id)
    flash('Deck deleted succesfully')
    return redirect(url_for('decks.index'))

@bp.route('/deck_editor/deck_save/<int:deck_id>', methods=('GET', 'POST'))
def deck_save(deck_id: int):
    name = request.form.get('name')
    description = request.form.get('description')
    Deckhandler.update_deck(name, description, deck_id)
    flash('Deck saved succesfully')
    return redirect(url_for('decks.index'))

@bp.route('/deck_editor/deck_editor', methods=('GET', 'POST')) 
def deck_editor():
    """ Arguments passed:
        deck_id: id or None
    """
    # Load deck if exists
    deck_id = request.args.get('deck_id')
    if deck_id:
        deck = Deckhandler.get_deck(deck_id)
        cards = Cardhandler.get_cards(deck_id)
    # No id means new deck
    else:
        test_user = Userhandler.get_test_user()
        deck_id = Deckhandler.new_deck(test_user)
        deck = Deckhandler.get_deck(deck_id)
        cards = Cardhandler.get_cards(deck_id)  # Will always be empty

    return render_template('decks/deck_editor.html', deck=deck, cards=cards)