from application.models.card import Card
from application.models.base import db
from application.handlers.deckhandler import Deckhandler
class Cardhandler:

    @staticmethod    
    def add_card(question: str, answer: str, deck_id: int) -> int:
        card = Card(question=question, answer=answer, deck_id=deck_id)
        db.session.add(card)
        db.session.commit()
        return card.id

    @staticmethod
    def new_card(deck_id: int) -> int:
        """ Create a new, empty card with placeholder values """
        placeholder_question = ""
        placeholder_answer = ""
        card_id = Cardhandler.add_card(placeholder_question, placeholder_answer, deck_id)
        return card_id

    @staticmethod
    def set_card_front(new_question: str, card_id: int):
        card = Card.query.get(card_id)
        card.question = new_question
        db.session.commit()

    @staticmethod
    def set_card_back(new_answer: str, card_id: int):
        card = Card.query.get(card_id)
        card.answer = new_answer
        db.session.commit()

    @staticmethod
    def get_card(card_id: int) -> dict:
        """ Get a single card from its id and return as dict """
        card = Card.query.get(card_id)
        return card

    @staticmethod
    def get_cards(deck_id):
        """ Get all cards that belong to a certain deck """
        cards = Card.query.filter_by(deck_id=deck_id).all()
        return cards

    @staticmethod
    def delete_card(card_id: int):
        card = Card.query.get(card_id)
        db.session.delete(card)
        db.session.commit()

    @staticmethod
    def create_cards(questions, answers, deck_id):
        for question, answer in zip(questions, answers):
            Cardhandler.add_card(question, answer, deck_id)

    @staticmethod
    def is_owned_by(user: object, card_id: int) -> bool:
        card = Cardhandler.get_card(card_id)
        deck = Deckhandler.get_deck(card.deck_id)
        return deck.user_id == user.id