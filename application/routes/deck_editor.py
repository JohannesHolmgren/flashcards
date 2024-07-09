"""
    This file contains all views for editing a deck.
"""

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_login import login_required, current_user

from application.handlers import Cardhandler, Deckhandler

from application.routes.page_stack import PageStack

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

@bp.route('/deck_editor/deck_editor/<int:deck_id>', methods=('GET', 'POST')) 
@login_required
def deck_editor(deck_id: int):
    # Deck can't be loaded
    if not deck_id:
        flash('The deck cannot be loaded')
        return redirect(url_for('decks.index'))
    # Deck does not belong to current user
    if not Deckhandler.is_owned_by(current_user, deck_id):
        flash("You don't have permission to edit this deck")
        return redirect(url_for('decks.index'))
    # Load deck
    deck = Deckhandler.get_deck(deck_id)
    cards = Cardhandler.get_cards(deck_id)
    return render_template('decks/deck_editor.html', deck=deck, cards=cards)

@bp.route('/deck_editor/new_deck/', methods=('GET', 'POST')) 
@login_required
def new_deck():
    # Create new deck
    deck_id = Deckhandler.new_deck(current_user)
    deck = Deckhandler.get_deck(deck_id)
    cards = Cardhandler.get_cards(deck_id)  # Will always be empty
    return render_template('decks/deck_editor.html', deck=deck, cards=cards)
