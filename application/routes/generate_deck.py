"""
    This file contains all views for generating a deck.
"""

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from application.handlers import Cardhandler, Deckhandler, Userhandler
from application.gpt import gpt_generate_deck

# Create blueprint for deck views
bp = Blueprint('generate_deck', __name__)

""" ---------- Helpers ---------- """

def dict_to_deck(deck_dict, user):
    """ Create a deck from a dict. Returns deck id """
    name = deck_dict.get('name')
    desc = deck_dict.get('description')
    questions = deck_dict.get('questions')
    answers = deck_dict.get('answers')
    deck_id = Deckhandler.add_deck(name, desc, user)
    Cardhandler.create_cards(questions, answers, deck_id)
    return deck_id

""" ---------- Routes ---------- """

@bp.route('/generate_deck/deck_from_text/', methods=('GET', 'POST'))
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

@bp.route('/generate_deck/cards_from_desc<int:deck_id>', methods=('GET', 'POST'))
def cards_from_desc(deck_id):
    # Save deck
    name = request.form.get('name')
    description = request.form.get('description')
    Deckhandler.update_deck(name, description, deck_id)
    # Generate cards
    raw_deck = gpt_generate_deck(description)
    if not raw_deck:
        flash('There was an error trying to generate your cards.')
        return redirect(url_for('deck_editor.deck_editor', deck_id=deck_id))
    for question, answer in zip(raw_deck.get('questions'), raw_deck.get('answers')):
        Cardhandler.add_card(question, answer, deck_id)
    
    deck = Deckhandler.get_deck(deck_id)
    return redirect(url_for('deck_editor.deck_editor', deck_id=deck.id))

@bp.route('/generate_deck/generate_deck')
def generate_deck():
    return render_template('decks/generate_deck.html')

@bp.route('/generate_deck/generate_deck_begin', methods=('GET', 'POST'))
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
    return redirect(url_for('deck_editor.deck_editor', deck_id=deck_id))