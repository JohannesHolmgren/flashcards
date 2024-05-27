''' 
    This file includes the class for a flashcard.

    A deck consists of cards. Initially empty
    
'''
from card import Card

class Deck:
    def __init__(self, name, description, id, user_id):
        self._id = id
        self.name = name
        self.description = description
        self._user_id = user_id
        self._cards = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name: str):
        if not isinstance(new_name, str):
            raise ValueError(f"Deck name must be of type 'str', got '{type(new_name)}'")
        self._name = new_name

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, new_description: str):
        if not isinstance(new_description, str):
            raise ValueError(f"Deck name must be of type 'str', got '{type(new_description)}'")
        self._description = new_description

    @property
    def id(self):
        return self._id
    
    @property
    def user_id(self):
        return self._user_id

    @property
    def cards(self):
        return self._cards

    def add_card(self, new_card:Card):
        if not isinstance(new_card, Card):
            raise ValueError(f"new_card must be of class 'Card', got '{type(new_card)}'")
        self._cards.append(new_card)
    
    def delete_card(self, card: Card):
        if not isinstance(card, Card):
            raise ValueError(f"card to delete must be of class 'Card', got '{type(card)}'")
        self._cards.remove(card)


""" ----- Test cases -----"""
def test_create_deck():
    deck = Deck("name", "description", 1, 1)
    card = Card("front", "back", 0, 0)
    deck.add_card(card)
    return(deck.name == "name"
           and deck.description == "description"
           and deck.cards[0] is card)

def test_add_bad_card():
    deck = Deck("name", "description", 1, 1)
    card = 123
    try:
        deck.add_card(card)
    except ValueError as E:
        return str(E) == "new_card must be of class 'Card', got '<class 'int'>'"
    return False

def test_delete_card():
    deck = Deck("name", "description", 1, 1)
    card = Card("front", "back", 0, 0)
    deck.add_card(card)
    deck.delete_card(card)
    return len(deck.cards) == 0
    
""" ----- Run test cases ----- """
if __name__ == "__main__":
    assert(test_create_deck())
    assert(test_add_bad_card())
    assert(test_delete_card())