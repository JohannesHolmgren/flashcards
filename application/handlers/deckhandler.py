from application.models.base import db
from application.models.deck import Deck

class Deckhandler:

    @staticmethod
    def add_deck(name: str, description: str, user: object):
        deck = Deck(name=name, description=description, user_id=user.id)
        db.session.add(deck)
        db.session.commit()
        return deck.id

    @staticmethod
    def new_deck(user: object):
        placeholder_name = ""
        placeholder_desc = ""
        deck_id = Deckhandler.add_deck(placeholder_name, placeholder_desc, user)
        return deck_id

    @staticmethod
    def set_deck_name(new_name: str, deck_id: int):
        deck = Deck.query.get(deck_id)
        deck.name = new_name
        db.session.commit()

    @staticmethod
    def set_deck_description(new_description: str, deck_id: int):
        deck = Deck.query.get(deck_id)
        deck.description = new_description
        db.session.commit()

    @staticmethod
    def update_deck(new_name: str, new_desc: str, deck_id: int):
        Deckhandler.set_deck_name(new_name, deck_id)
        Deckhandler.set_deck_description(new_desc, deck_id)

    @staticmethod
    def delete_deck(deck_id: int):
        deck = Deck.query.get(deck_id)
        db.session.delete(deck)
        db.session.commit()

    @staticmethod
    def get_deck(deck_id):
        deck = Deck.query.get(deck_id)
        return deck

    @staticmethod
    def get_decks(user: object):
        """ Get all decks that belong to a certain user """
        decks = Deck.query.filter_by(user_id=user.id).all()
        return decks
    