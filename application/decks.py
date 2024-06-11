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

from .models import db
from .models.user import User
from .models.card import Card
from .models.deck import Deck

""" Functions """
def add_deck(name: str, description: str, user_id: int):
    deck = Deck(name=name, description=description, user_id=user_id)
    db.session.add(deck)
    db.session.commit()
    return deck.id

def new_deck(user_id):
    """ Create a new, empty deck with placeholder values """
    placeholder_name = ""
    placeholder_desc = ""
    deck_id = add_deck(placeholder_name, placeholder_desc, user_id)
    return deck_id

def set_deck_name(new_name: str, deck_id: int):
    deck = Deck.query.get(deck_id)
    deck.name = new_name
    db.session.commit()

def set_deck_description(new_description: str, deck_id: int):
    deck = Deck.query.get(deck_id)
    deck.description = new_description
    db.session.commit()

def update_deck(new_name: str, new_desc: str, deck_id: int):
    set_deck_name(new_name, deck_id)
    set_deck_description(new_desc, deck_id)

def delete_deck(deck_id: int):
    deck = Deck.query.get(deck_id)
    db.session.delete(deck)
    db.session.commit()

def deck_to_dict(deck: tuple) -> dict:
    new_dict = {
            'id': deck.id,
            'name': deck.name,
            'description': deck.description,
            'user_id': deck.user_id
        }
    return new_dict

def card_to_dict(card: tuple) -> dict:
    new_dict = {
        'id': card.id,
        'front': card.question,
        'back': card.answer,
        'deck_id': card.deck_id
    }
    return new_dict

def get_deck(deck_id):
    deck = Deck.query.get(deck_id)
    return deck_to_dict(deck)

def get_decks(user_id):
    """ Get all decks that belong to a certain user """
    decks = Deck.query.filter_by(user_id=user_id).all()
    deck_dicts = []
    for deck in decks:
        deck_dicts.append(deck_to_dict(deck))
    return deck_dicts

def add_card(question: str, answer: str, deck_id: int) -> int:
    card = Card(question=question, answer=answer, deck_id=deck_id)
    db.session.add(card)
    db.session.commit()
    return card.id

def new_card(deck_id: int) -> int:
    """ Create a new, empty card with placeholder values """
    placeholder_question = ""
    placeholder_answer = ""
    card_id = add_card(placeholder_question, placeholder_answer, deck_id)
    return card_id

def set_card_front(new_question: str, card_id: int):
    card = Card.query.get(card_id)
    card.question = new_question
    db.session.commit()

def set_card_back(new_answer: str, card_id: int):
    card = Card.query.get(card_id)
    card.answer = new_answer
    db.session.commit()

def get_card(card_id: int) -> dict:
    """ Get a single card from its id and return as dict """
    card = Card.query.get(card_id)
    return card_to_dict(card)

def get_cards(deck_id):
    """ Get all cards that belong to a certain deck """
    cards = Card.query.filter_by(deck_id=deck_id).all()
    # Convert to dictionary
    card_dicts = []
    for card in cards:
        card_dicts.append(card_to_dict(card))
    return card_dicts

def delete_card(card_id: int):
    card = Card.query.get(card_id)
    db.session.delete(card)
    db.session.commit()

def create_cards(questions, answers, deck_id):
    for question, answer in zip(questions, answers):
        add_card(question, answer, deck_id)

def dict_to_deck(deck_dict, user_id):
    """ Create a deck from a dict. Returns deck id """
    name = deck_dict.get('name')
    desc = deck_dict.get('description')
    questions = deck_dict.get('questions')
    answers = deck_dict.get('answers')
    deck_id = add_deck(name, desc, user_id)
    create_cards(questions, answers, deck_id)
    return deck_id


""" ---------- Index ---------- """
# Create blueprint for deck views
bp = Blueprint('decks', __name__)

# A simple start page
@bp.route('/')
def home():
    return redirect(url_for('decks.index'))

TEST_USER = 0
@bp.route('/decks', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        add_deck(name, description, TEST_USER)

    decks = get_decks(TEST_USER)
    return render_template('decks/index.html', decks=decks)

""" ---------- Deck editor ---------- """

@bp.route('/decks/deck_delete/<int:deck_id>', methods=('GET', 'POST'))
def deck_delete(deck_id: int):
    delete_deck(deck_id)
    flash('Deck deleted succesfully')
    return redirect(url_for('decks.index'))

@bp.route('/decks/deck_save/<int:deck_id>', methods=('GET', 'POST'))
def deck_save(deck_id: int):
    name = request.form.get('name')
    description = request.form.get('description')
    update_deck(name, description, deck_id)
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
        deck = get_deck(deck_id)
        cards = get_cards(deck_id)
    # No id means new deck
    else:
        deck_id = new_deck(TEST_USER)
        deck = get_deck(deck_id)
        cards = get_cards(deck_id)  # Will always be empty

    return render_template('decks/deck_editor.html', deck=deck, cards=cards)

""" ---------- Card editor ---------- """

@bp.route('/decks/card_delete/<int:card_id>', methods=('GET', 'POST'))
def card_delete(card_id: int):
    deck_id = get_card(card_id).get('deck_id')
    delete_card(card_id)
    return redirect(url_for('decks.deck_editor', deck_id=deck_id))

@bp.route('/decks/card_save/<int:card_id>', methods=('GET', 'POST'))
def card_save(card_id: int):
    front = request.form.get('front')
    back = request.form.get('back')
    deck_id = request.form.get('deck_id')
    set_card_front(front, card_id)
    set_card_back(back, card_id)
    return redirect(url_for('decks.deck_editor', deck_id=deck_id))

@bp.route('/decks/card_editor', methods=('GET', 'POST'))
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
        card = get_card(card_id)
    else:
        card_id = new_card(deck_id)
        card = get_card(card_id)
    
    return render_template('decks/card_editor.html', card=card)


""" ---------- Play a deck of cards ---------- """
card_ids = []

@bp.route('/decks/init_play_all<int:deck_id>', methods=('GET', 'POST'))
def init_play_all(deck_id):
    global card_ids
    card_ids = [card.get('id') for card in get_cards(deck_id)]
    random.shuffle(card_ids)
    return redirect(url_for('decks.play_new_card', deck_id=deck_id))

@bp.route('/decks/play_new_card<int:deck_id>')
def play_new_card(deck_id):
    if len(card_ids) == 0:
        return redirect(url_for('decks.play_end', deck_id=deck_id))
    
    card_id = card_ids.pop()
    return redirect(url_for('decks.play_card_front', card_id=card_id))

@bp.route('/decks/play_card_front<int:card_id>', methods=('GET', 'POST'))
def play_card_front(card_id):
    card = get_card(card_id)
    return render_template('decks/play_card_front.html', card=card)

@bp.route('/decks/play_card_back<int:card_id>', methods=('GET', 'POST'))
def play_card_back(card_id):
    card = get_card(card_id)
    return render_template('decks/play_card_back.html', card=card)

@bp.route('/decks/play_end<int:deck_id>', methods=('GET', 'POST'))
def play_end(deck_id):
    deck = get_deck(deck_id)
    return render_template('decks/play_end.html', deck=deck)


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
    deck_id = add_deck(name=raw_deck.get('name'), description=raw_deck.get('description'), user_id=TEST_USER)
    for question, answer in zip(raw_deck.get('questions'), raw_deck.get('answers')):
        add_card(question, answer, deck_id)
    return redirect(url_for('decks.index'))

@bp.route('/decks/cards_from_desc<int:deck_id>', methods=('GET', 'POST'))
def cards_from_desc(deck_id):
    # Save deck
    name = request.form.get('name')
    description = request.form.get('description')
    update_deck(name, description, deck_id)
    # Generate cards
    raw_deck = gpt_generate_deck(description)
    if not raw_deck:
        flash('There was an error trying to generate your cards.')
        return redirect(url_for('decks.deck_editor', deck_id=deck_id))
    for question, answer in zip(raw_deck.get('questions'), raw_deck.get('answers')):
        add_card(question, answer, deck_id)
    
    deck = get_deck(deck_id)
    return redirect(url_for('decks.deck_editor', deck_id=deck.get('id')))

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
    deck_id = dict_to_deck(raw_deck, TEST_USER)
    flash('Deck generated successfully')
    return redirect(url_for('decks.deck_editor', deck_id=deck_id))