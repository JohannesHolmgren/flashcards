"""
    This file includes the code for the deck-view page (or startpage).

    Blueprints are used to organize different views.
    For this part, a blueprint is used to group
    - deck-view page
    - create deck
    - create card
    - practice deck / cards

"""

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

def get_decks(user_id):
    # Get all decks
    db = get_db()
    decks = db.execute(
        # "SELECT * FROM deck WHERE user_id = ?",
        "SELECT * FROM deck"
        # (user_id)
    ).fetchall()

    print('number of decks', len(decks))
    # Convert to dictionary
    deck_dicts = []
    for deck in decks:
        new_dict = {
            'id': deck[0],
            'name': deck[1],
            'description': deck[2],
            'user_id': deck[3]
        }
        deck_dicts.append(new_dict)
    return deck_dicts

""" Views """

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
    print(len(decks))
    return render_template('decks/index.html', decks=decks)
