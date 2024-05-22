"""
    This file includes the class for a user.

    A user has:
    - a username
    - an arbitrary number of decks


    A possible improvment:
    Decks could be saved in a dict instead, with name as key.
    
"""
from deck import Deck

class User:
    def __init__(self, name):
        self.username = name
        self._decks = []

    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, name):
        if not isinstance(name, str):
            raise ValueError(f"username must be of class 'Deck', got '{type(name)}'")
        self._username = name

    def add_deck(self, new_deck):
        if not isinstance(new_deck, Deck):
            raise ValueError(f"new_deck must be of class 'Deck', got '{type(new_deck)}'")
        self._decks.append(new_deck)

    @property
    def decks(self):
        return self._decks


""" ----- Test Cases ----- """
def test_create_user():
    username = "hej123"
    user = User(username)
    return user.username == username

def test_add_deck():
    user = User("hej123")
    deck = Deck("name", "decription")
    user.add_deck(deck)
    return user.decks[0] == deck and len(user.decks) == 1

def test_add_bad_deck():
    user = User("hej123")
    deck = 123
    try:
        user.add_deck(deck)
    except ValueError as E:
        return str(E) == "new_deck must be of class 'Deck', got '<class 'int'>'"

if __name__ == "__main__":
    assert(test_create_user())
    assert(test_add_deck())
    assert(test_add_bad_deck())