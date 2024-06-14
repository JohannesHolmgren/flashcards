"""
    This file contains all views for playing a deck.
"""

import random
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from application.models.cardhandler import Cardhandler
from application.models.deckhandler import Deckhandler

# Create blueprint for deck views
bp = Blueprint('play', __name__)

card_ids = []
@bp.route('/play/init_play_all<int:deck_id>', methods=('GET', 'POST'))
def init_play_all(deck_id):
    global card_ids
    card_ids = [card.id for card in Cardhandler.get_cards(deck_id)]
    random.shuffle(card_ids)
    return redirect(url_for('play.play_new_card', deck_id=deck_id))

@bp.route('/play/play_new_card<int:deck_id>')
def play_new_card(deck_id):
    if len(card_ids) == 0:
        return redirect(url_for('play.play_end', deck_id=deck_id))
    
    card_id = card_ids.pop()
    return redirect(url_for('play.play_card_front', card_id=card_id))

@bp.route('/play/play_card_front<int:card_id>', methods=('GET', 'POST'))
def play_card_front(card_id):
    card = Cardhandler.get_card(card_id)
    print(card)
    return render_template('decks/play_card_front.html', card=card)

@bp.route('/play/play_card_back<int:card_id>', methods=('GET', 'POST'))
def play_card_back(card_id):
    card = Cardhandler.get_card(card_id)
    return render_template('decks/play_card_back.html', card=card)

@bp.route('/play/play_end<int:deck_id>', methods=('GET', 'POST'))
def play_end(deck_id):
    deck = Deckhandler.get_deck(deck_id)
    return render_template('decks/play_end.html', deck=deck)