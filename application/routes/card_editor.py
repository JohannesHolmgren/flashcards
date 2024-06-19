from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_login import login_required

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

@bp.route('/card_editor', methods=('GET', 'POST'))
@login_required
def card_editor():
    """
        Arguments passed:
        card_id: id or None
    """
    # Load card if exists else create new card
    card_id = request.args.get('card_id')
    deck_id = request.args.get('deck_id')
    if not deck_id:
        flash('NO DECK ID! WARNING')
    if card_id:
        card = Cardhandler.get_card(card_id)
    else:
        card_id = Cardhandler.new_card(deck_id)
        card = Cardhandler.get_card(card_id)
    
    return render_template('decks/card_editor.html', card=card)