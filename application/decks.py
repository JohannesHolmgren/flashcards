"""
    This file includes the code for the deck-view page (or startpage).

    Blueprints are used to organize different views.
    For this part, a blueprint is used to group
    - deck-view page
    - create deck
    - create card
    - practice deck / cards

"""
import random
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from application.gpt import gpt_generate_deck
from .models import Deckhandler, Cardhandler, Userhandler

""" ---------- Test user during testing ---------- """

def dict_to_deck(deck_dict, user):
    """ Create a deck from a dict. Returns deck id """
    name = deck_dict.get('name')
    desc = deck_dict.get('description')
    questions = deck_dict.get('questions')
    answers = deck_dict.get('answers')
    deck_id = Deckhandler.add_deck(name, desc, user)
    Cardhandler.create_cards(questions, answers, deck_id)
    return deck_id

""" ---------- Index ---------- """
# Create blueprint for deck views
bp = Blueprint('decks', __name__)

# A simple start page
@bp.route('/')
def home():
    return redirect(url_for('decks.index'))

@bp.route('/decks', methods=('GET', 'POST'))
def index():
    test_user = Userhandler.get_test_user()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        Deckhandler.add_deck(name, description, test_user)

    decks = Deckhandler.get_decks(test_user)
    return render_template('decks/index.html', decks=decks)

""" ---------- Deck editor ---------- """

@bp.route('/decks/deck_delete/<int:deck_id>', methods=('GET', 'POST'))
def deck_delete(deck_id: int):
    Deckhandler.delete_deck(deck_id)
    flash('Deck deleted succesfully')
    return redirect(url_for('decks.index'))

@bp.route('/decks/deck_save/<int:deck_id>', methods=('GET', 'POST'))
def deck_save(deck_id: int):
    name = request.form.get('name')
    description = request.form.get('description')
    Deckhandler.update_deck(name, description, deck_id)
    flash('Deck saved succesfully')
    return redirect(url_for('decks.index'))

@bp.route('/decks/deck_editor', methods=('GET', 'POST')) 
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

""" ---------- Generate decks of cards ---------- """
@bp.route('/decks/deck_from_text/', methods=('GET', 'POST'))
def deck_from_text():
    file = request.files['file']
    file_content = file.read()
    text = file_content.decode('utf-8')
    raw_deck = gpt_generate_deck(text)
    if not raw_deck:
        flash('There was an error trying to generate your deck.')
        return redirect(url_for('decks.index'))
    test_user = Userhandler.get_test_user()
    deck_id = Deckhandler.add_deck(name=raw_deck.get('name'), description=raw_deck.get('description'), user=test_user)
    for question, answer in zip(raw_deck.get('questions'), raw_deck.get('answers')):
        Cardhandler.add_card(question, answer, deck_id)
    return redirect(url_for('decks.index'))

@bp.route('/decks/cards_from_desc<int:deck_id>', methods=('GET', 'POST'))
def cards_from_desc(deck_id):
    # Save deck
    name = request.form.get('name')
    description = request.form.get('description')
    Deckhandler.update_deck(name, description, deck_id)
    # Generate cards
    raw_deck = gpt_generate_deck(description)
    if not raw_deck:
        flash('There was an error trying to generate your cards.')
        return redirect(url_for('decks.deck_editor', deck_id=deck_id))
    for question, answer in zip(raw_deck.get('questions'), raw_deck.get('answers')):
        Cardhandler.add_card(question, answer, deck_id)
    
    deck = Deckhandler.get_deck(deck_id)
    return redirect(url_for('decks.deck_editor', deck_id=deck.id))

@bp.route('/decks/generate_deck')
def generate_deck():
    return render_template('decks/generate_deck.html')

@bp.route('/decks/generate_deck_begin', methods=('GET', 'POST'))
def generate_deck_begin():
    quantities = {
        'few': 10,
        'medium': 25,
        'many': 50
    }
    prompt = request.form.get('prompt')
    focus_areas = request.form.getlist('focus_areas')
    quantity = request.form.get('quantity')
    n_cards = quantities[quantity]
    raw_deck = gpt_generate_deck(prompt, n_cards, focus_areas)
    if not raw_deck:
        flash('There was an error trying to generate your deck.')
        return redirect(url_for('decks.index'))
    test_user = Userhandler.get_test_user()
    deck_id = dict_to_deck(raw_deck, test_user)
    flash('Deck generated successfully')
    return redirect(url_for('decks.deck_editor', deck_id=deck_id))