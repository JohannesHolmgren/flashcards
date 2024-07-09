from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_login import login_required, current_user

from application.handlers import Cardhandler

# Create blueprint for deck views
bp = Blueprint('card_editor', __name__)

""" ---------- Routes ---------- """

@bp.route('/card_editor/card_delete/<int:card_id>', methods=('GET', 'POST'))
@login_required
def card_delete(card_id: int):
    card = Cardhandler.get_card(card_id)
    deck_id = card.deck_id
    Cardhandler.delete_card(card_id)
    return redirect(url_for('deck_editor.deck_editor', deck_id=deck_id))

@bp.route('/card_editor/card_save/<int:card_id>', methods=('GET', 'POST'))
@login_required
def card_save(card_id: int):
    front = request.form.get('front')
    back = request.form.get('back')
    deck_id = request.form.get('deck_id')
    Cardhandler.set_card_front(front, card_id)
    Cardhandler.set_card_back(back, card_id)
    return redirect(url_for('deck_editor.deck_editor', deck_id=deck_id))

@bp.route('/card_editor/card_editor<int:card_id>', methods=('GET', 'POST'))
@login_required
def card_editor(card_id):
    # Card can't be loaded
    if not card_id:
        flash('The card cannot be loaded')
        return redirect(url_for('decks.index'))
    # Card does not belong to current user
    if not Cardhandler.is_owned_by(current_user, card_id):
        flash("You don't have permission to edit this card")
        return redirect(url_for('decks.index'))
    # Load card
    card = Cardhandler.get_card(card_id)
    return render_template('decks/card_editor.html', card=card)

@bp.route('/card_editor/new_card<int:deck_id>', methods=('GET', 'POST'))
@login_required
def new_card(deck_id):
    if not deck_id:
        flash('NO DECK ID! WARNING')
    # Create new card
    card_id = Cardhandler.new_card(deck_id)
    card = Cardhandler.get_card(card_id)
    return render_template('decks/card_editor.html', card=card)