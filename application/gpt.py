"""
    This file handles the gpt-API
"""
from openai import OpenAI
import json

gpt_client = OpenAI()

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

def generate_deck(text: str, focus_areas=[]):
    """ Generate a deck of flashcards (questions and answers) 
        from a text. 
        text (str): the text to generate flashcards from

        Return: A python dict on the form: 
                {
                    'name': name,
                    'description': description, 
                    'fronts': [front1, front2...],
                    'backs': [back1, back2...]
                }
    """
    msg_create_flashcards = '''
        You are an assistant to create a deck of flashcards from texts. Return a JSON 
        object with a key 'name' with the name of the deck, 
        a key 'description' with the description of the deck,
        a key 'questions' with a list of the questions 
        and a key 'answers' with a list of the answers to the question. 
        The two lists must be the same length
    '''
    msg_focus_on = 'focus on ' + ','.join(focus_areas)
    messages = []
    messages.append(msg_create_flashcards)
    messages.append(msg_focus_on)

    res = ask(text, messages=messages, as_json=True)
    print(res)
    return json.loads(res)


if __name__ == '__main__':
    print(generate_deck(
        "In a world filles with food you can only eat fruits. Stones are very hard and you should never throw them at other people, even if you really feel like it", focus_areas=['fruits'])
        )