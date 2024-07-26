"""
    This file contains all views for playing a deck.
"""

import random
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_login import login_required

from application.handlers import Cardhandler, Deckhandler

# Create blueprint for deck views
bp = Blueprint('play', __name__)

# Keeps the deck's card while in a play-through
card_ids = []
# Used to keep track of the progress of the play-through
n_cards_played = 0

class PlayThrough:
    ''' A class representing a playthrough of a deck. '''

    def __init__(self, deck_id):
        self.deck_id = deck_id
        self.card_ids = [card.id for card in Cardhandler.get_cards(deck_id)]
        random.shuffle(self.card_ids)
        self.n_cards_played = 0
        self.n_total_cards = len(self.card_ids)
    
    def next_card(self):
        if len(self.card_ids) == 0:
            return None
        self.n_cards_played += 1
        return self.card_ids.pop()
    

# Global playthrough
playthrough = None

@bp.route('/play/init_play_all<int:deck_id>', methods=('GET', 'POST'))
@login_required
def init_play_all(deck_id):
    # global card_ids
    # card_ids = [card.id for card in Cardhandler.get_cards(deck_id)]
    # random.shuffle(card_ids)
    global playthrough
    playthrough = PlayThrough(deck_id)

    return redirect(url_for('play.play_new_card', deck_id=deck_id))

@bp.route('/play/play_new_card<int:deck_id>')
@login_required
def play_new_card(deck_id):
    
    # Get card and increase number of cards played
    card_id = playthrough.next_card()
    if not card_id:
        return redirect(url_for('play.play_end', deck_id=deck_id))

    n_cards_played = playthrough.n_cards_played
    n_total_cards = playthrough.n_total_cards

    return redirect(url_for(
        'play.play_card_front',
        card_id=card_id,
        n_cards_played=n_cards_played,
        n_total_cards=n_total_cards
    ))

@bp.route('/play/play_card_front<int:card_id><int:n_cards_played><int:n_total_cards>', methods=('GET', 'POST'))
@login_required
def play_card_front(card_id, n_cards_played, n_total_cards):
    card = Cardhandler.get_card(card_id)
    return render_template('decks/play_card_front.html', card=card, n_cards_played=n_cards_played, n_total_cards=n_total_cards)

@bp.route('/play/play_card_back<int:card_id><int:n_cards_played><int:n_total_cards>', methods=('GET', 'POST'))
@login_required
def play_card_back(card_id, n_cards_played, n_total_cards):
    card = Cardhandler.get_card(card_id)
    return render_template('decks/play_card_back.html', card=card, n_cards_played=n_cards_played, n_total_cards=n_total_cards)

@bp.route('/play/play_end<int:deck_id>', methods=('GET', 'POST'))
@login_required
def play_end(deck_id):
    deck = Deckhandler.get_deck(deck_id)
    return render_template('decks/play_end.html', deck=deck)