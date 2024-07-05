"""
    This file contains all views for generating a deck.
"""

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from flask_login import login_required, current_user

from application.handlers import Cardhandler, Deckhandler
from application.gpt import gpt_generate_deck
from application.engine import pdf_reader
from application.engine.handle_markdown import markdown_to_html

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

def get_extension(filename: str) -> str:
    return filename.rsplit('.', 1)[1].lower()

def is_pdf(filename: str) -> bool:
    if not '.' in filename: return False
    return get_extension(filename) == 'pdf'

def is_markdown(filename: str) -> bool:
    if not '.' in filename: return False
    return get_extension(filename) == 'md'

def is_txt(filename: str) -> bool:
    if not '.' in filename: return False
    return get_extension(filename) == 'txt'

""" ---------- Routes ---------- """

@bp.route('/generate_deck/deck_from_file/', methods=('GET', 'POST'))
@login_required
def deck_from_file():
    # Get input
    file = request.files['file']
    n_cards = int(request.form.get('n_cards'))
    prompt = request.form.get('prompt')
    start_page = int(request.form.get('start-page'))
    end_page = int(request.form.get('end-page'))
    # Decode file content
    if is_pdf(file.filename):
        text = pdf_reader.extract_text(file, start_page, end_page)
    elif is_markdown(file.filename) or is_txt(file.filename):
        file_content = file.read()
        text = file_content.decode('utf-8')
    else:
        flash('Invalid file')
        return redirect(url_for('generate_deck.from_file'))
    # Generate deck
    raw_deck = gpt_generate_deck(text, n_cards, [prompt])
    if not raw_deck:
        flash('There was an error trying to generate your deck.')
        return redirect(url_for('decks.index'))
    deck_id = Deckhandler.add_deck(name=raw_deck.get('name'), description=raw_deck.get('description'), user=current_user)
    for question, answer in zip(raw_deck.get('questions'), raw_deck.get('answers')):
        # Convert markdown to html
        if is_markdown(file.filename):
            question = markdown_to_html(question)
            answer = markdown_to_html(answer)
        Cardhandler.add_card(question, answer, deck_id)
    return redirect(url_for('decks.index'))

@bp.route('/generate_deck/number_of_pdf_pages', methods=['POST'])
def get_number_of_pdf_pages():
    # Check if request correct with file
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    # Check if file selected
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    # Get page range if is pdf
    if file and is_pdf(file.filename):
        page_range = pdf_reader.get_page_range(file)
        return jsonify({"page_range": page_range})
    return jsonify({"error": "Not pdf"}), 400

@bp.route('/generate_deck/cards_from_desc<int:deck_id>', methods=('GET', 'POST'))
@login_required
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

@bp.route('/generate_deck/from_prompt')
@login_required
def from_prompt():
    return render_template('decks/generate_deck.html')

@bp.route('/generate_deck/from_file')
@login_required
def from_file():
    return render_template('generate_deck/from_file.html')

@bp.route('/generate_deck/generate_deck_begin', methods=('GET', 'POST'))
@login_required
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
    deck_id = dict_to_deck(raw_deck, current_user)
    flash('Deck generated successfully')
    return redirect(url_for('deck_editor.deck_editor', deck_id=deck_id))