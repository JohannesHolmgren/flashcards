"""
    This file handles the gpt-API
"""
from openai import OpenAI
import json
from json import JSONDecodeError
from datetime import datetime
import os

gpt_client = OpenAI()

def log_jsonerror(text, n_cards, focus_areas, res):
    """ Write a log with all information to logs/gpt_jsonerror. """
    dir = os.path.dirname('logs/gpt_jsonerror/')
    if dir and not os.path.exists(dir):
        os.makedirs(dir)
    timestamp = datetime.now()
    log_name = timestamp.strftime('%Y%m%d_%H%M%S_%f')
    labels = ['Input text', 'n_cards', 'focus_areas', 'Output text']
    to_log = [str(item) for item in [text, n_cards, focus_areas, res]]
    with open(f'logs/gpt_jsonerror/{log_name}.log', 'w') as f:
        for label, item in zip(labels, to_log):
            f.write(f'=========== {label} ===========')
            f.write('\n\n')
            f.write(item)
            f.write('\n\n')

def ask(input_prompt: str, messages:list =[], model: str='gpt-3.5-turbo', as_json=False):
    """ Calls on the model and returns its answer as a json-object.
        input_prompt (str): The question, text to respond to.
        messages (list):    additional messages to adjust the behavior
                            of the model as a list of strings.
        model (str):        'gpt-3.5-turbo' (default) |'gpt-4o'.
        as_json (bool):     whether to return in json format or not. Must mention 'JSON'
                            somewhere in messages if set to True

        Return: The reply as a string
    """
    # Messages on expected format
    msgs = [{'role': 'system', 'content': message} for message in messages]
    msgs.append({'role': 'user', 'content': input_prompt})
    completion = gpt_client.chat.completions.create(
        model=model,
        response_format=None,
        messages=msgs
    )
    return completion.choices[0].message.content

def gpt_generate_deck(text:str, n_cards: int=None, focus_areas:list=[]) -> str:
    """ Generate a deck of flashcards (questions and answers) 
        from a text. 
        text:        The text to generate flashcards from
        n_cards:     How many cards to generate (circa) or None to
                     let the model decide. Note that a max roof of 999 cards is set
        focus_areas: A list of strings of specifics, e.g. dates, names etc.

        Return: A python dict on the form: 
                {
                    'name': name,
                    'description': description, 
                    'fronts': [front1, front2...],
                    'backs': [back1, back2...]
                }
    """
    N_MAX_CARDS = 999
    msg_create_flashcards = '''
        You are an assistant to create a deck of flashcards from texts. Return only a JSON 
        object with a key 'name' with the name of the deck, 
        a key 'description' with the description of the deck,
        a key 'questions' with a list of the questions 
        and a key 'answers' with a list of the answers to the question. 
        The two lists must be the same length. Don't add anything around the JSON object.
    '''
    messages = []
    messages.append(msg_create_flashcards)
    if not is_valid_input(text):
        return None
    if is_valid_focus_areas(focus_areas):
        msg_focus_on = 'focus on ' + ','.join(focus_areas)
        messages.append(msg_focus_on)
    if is_valid_number(n_cards):
        # Cap number of cards if too many
        n_cards = min(n_cards, N_MAX_CARDS)
        msg_amount_cards = f"Generate {n_cards} cards"
        messages.append(msg_amount_cards)
    # Generate deck on JSON shape.
    # Sometimes the output doesn't work to convert to json,
    # which is why a JSONDecodeError may occur
    try:
        res = ask(text, messages=messages, as_json=True)
        deck = json.loads(res)
    except JSONDecodeError as E:
        log_jsonerror(text, n_cards, focus_areas, res)
        return None
    if not is_valid_deck(deck):
        log_jsonerror(text, n_cards, focus_areas, res)
        return None
    return deck

def is_valid_input(text: str):
    """ Check if the input text is valid.
        Valid if it's a string
    """
    return isinstance(text, str)

def is_valid_focus_areas(focus_areas: list):
    """ Check if focus_areas is valid.
        Valid if it's a list containing strings
    """
    if not isinstance(focus_areas, list):
        return False
    if not all([isinstance(area, str) for area in focus_areas]):
        return False
    if not len(focus_areas) > 0:
        return False
    return True

def is_valid_number(n_cards: int):
    """ Check if n_cards is valid.
        Valid if it's an integer and not None
    """
    return isinstance(n_cards, int)

def is_valid_deck(deck: dict):
    """ Check if a dict is valid.
        Valid if contains all expected keys and
        if both questions and answers are lists 
    """
    expected_keys = ['name', 'description', 'questions', 'answers']
    existing_keys = [True if key in deck.keys() else False for key in expected_keys]
    if not all(existing_keys):
        return False
    if not isinstance(deck.get('questions'), list):
        return False
    if not isinstance(deck.get('answers'), list):
        return False
    return True


if __name__ == '__main__':
    print(gpt_generate_deck(
        "In a world filles with food you can only eat fruits. Stones are very hard and you should never throw them at other people, even if you really feel like it", focus_areas=['fruits'])
        )