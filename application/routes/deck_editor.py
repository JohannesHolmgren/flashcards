"""
    This file contains all views for editing a deck.
"""

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_login import login_required, current_user

from application.handlers import Cardhandler, Deckhandler

# Create blueprint for deck views
bp = Blueprint('deck_editor', __name__)

""" ---------- Routes ---------- """

@bp.route('/deck_editor/deck_delete/<int:deck_id>', methods=('GET', 'POST'))
@login_required
def deck_delete(deck_id: int):
    Deckhandler.delete_deck(deck_id)
    flash('Deck deleted succesfully')
    return redirect(url_for('decks.index'))

@bp.route('/deck_editor/deck_save/<int:deck_id>', methods=('GET', 'POST'))
@login_required
def deck_save(deck_id: int):
    name = request.form.get('name')
    description = request.form.get('description')
    Deckhandler.update_deck(name, description, deck_id)
    flash('Deck saved succesfully')
    return redirect(url_for('decks.index'))

@bp.route('/deck_editor/deck_editor', methods=('GET', 'POST')) 
@login_required
def deck_editor():
    """ Arguments passed:
        deck_id: id or None
    """
    # Load deck if exists
    deck_id = request.args.get('deck_id')
    if deck_id:
        if not Deckhandler.is_owned_by(current_user, deck_id):
            flash("You don't have permission to edit this deck")
            return redirect(url_for('decks.index'))
        deck = Deckhandler.get_deck(deck_id)
        cards = Cardhandler.get_cards(deck_id)
    # No id means new deck
    else:
        deck_id = Deckhandler.new_deck(current_user)
        deck = Deckhandler.get_deck(deck_id)
        cards = Cardhandler.get_cards(deck_id)  # Will always be empty

    return render_template('decks/deck_editor.html', deck=deck, cards=cards)