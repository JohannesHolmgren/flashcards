"""
    This file includes the code for the deck-view page (or startpage).

    Blueprints are used to organize different views.
    For this part, a blueprint is used to group
    - deck-view page
    - create deck
    - create card
    - practice deck / cards

"""
import json
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from application.db import get_db

""" Create blueprint for these views """
bp = Blueprint('decks', __name__)

""" Functions """
def add_deck(name: str, description: str, user_id: int):
    db = get_db()
    db.execute(
        "INSERT INTO deck (name, description, user_id) VALUES (?, ?, ?)", 
        (name, description, user_id)
    )
    db.commit()
    deck_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]
    return deck_id

def new_deck(user_id):
    """ Create a new, empty deck with placeholder values """
    placeholder_name = ""
    placeholder_desc = ""
    deck_id = add_deck(placeholder_name, placeholder_desc, user_id)
    return deck_id


def set_deck_name(new_name: str, deck_id: int):
    db = get_db()
    db.execute(
        "UPDATE deck SET name = ? WHERE id = ?",
        (new_name, deck_id)
    )
    db.commit()

def set_deck_description(new_desc: str, deck_id: int):
    db = get_db()
    db.execute(
        "UPDATE deck SET description = ? WHERE id = ?",
        (new_desc, deck_id)
    )
    db.commit()

def delete_deck(deck_id: int):
    db = get_db()
    db.execute(
        "DELETE FROM deck where id = ?",
        (deck_id,)
    )
    db.commit()

def deck_to_dict(deck: tuple) -> dict:
    new_dict = {
            'id': deck[0],
            'name': deck[1],
            'description': deck[2],
            'user_id': deck[3]
        }
    return new_dict

def card_to_dict(card: tuple) -> dict:
    new_dict = {
        'id': card[0],
        'front': card[1],
        'back': card[2],
        'deck_id': card[3]
    }
    return new_dict

def get_deck(deck_id):
    db = get_db()
    deck = db.execute("SELECT * FROM deck WHERE id = ?", (deck_id,)).fetchone()
    return deck_to_dict(deck)

def get_decks(user_id):
    """ Get all decks that belong to a certain user """
    # Get decks from database
    db = get_db()
    decks = db.execute(
        # "SELECT * FROM deck WHERE user_id = ?",
        "SELECT * FROM deck"
        # (user_id)
    ).fetchall()
    # Convert to dictionary
    deck_dicts = []
    for deck in decks:
        deck_dicts.append(deck_to_dict(deck))
    return deck_dicts

def get_cards(deck_id):
    """ Get all cards that belong to a certain deck """
    # Get cards from database
    db = get_db()
    cards = db.execute(
        "SELECT * FROM card WHERE deck_id = ?", 
        (deck_id,)
    ).fetchall()
    # Convert to dictionary
    card_dicts = []
    for card in cards:
        card_dicts.append(card_to_dict(card))
    return card_dicts

""" ----- Views ----- """
"""
    The index view is where all the decks are shown.
"""
TEST_USER = 0
@bp.route('/decks', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        add_deck(name, description, TEST_USER)

    decks = get_decks(TEST_USER)
    return render_template('decks/index.html', decks=decks)

"""
    decks/editor view is where a deck is edited and the cards are shown
"""
@bp.route('/decks/editor', methods=('GET', 'POST'))
def editor():
    """ Arguments passed:
    """
    # Handle update of deck
    if request.method == 'POST':
        action = request.form.get('action')
        deck_id = request.form.get('id')
        deck_name = request.form.get('name')
        deck_description = request.form.get('description')
        # Save deck
        if action == 'save':
            set_deck_name(deck_name, deck_id)
            set_deck_description(deck_description, deck_id)
            return redirect(url_for('decks.index'))
        # Delete deck
        if action == 'delete':
            delete_deck(deck_id)
            return redirect(url_for('decks.index'))

    # Load deck if existed
    deck_id = request.args.get('deck_id')
    if deck_id:
        deck = get_deck(deck_id)
        cards = get_cards(deck_id)
    # No id means new deck
    else:
        deck_id = new_deck(TEST_USER)
        deck = get_deck(deck_id)
        cards = []

    return render_template('decks/editor.html', deck=deck, cards=cards)