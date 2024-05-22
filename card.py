"""
    This file includes the class for a flashcard.

    A flashcard is represented by the following information:
    - A frontside
    - A backside
    - Status of knowledge as a scale 1-5
        - 1: first time
        - 2: tomorrow
        - 3: three days
        - 4: one week
        - 5: two weeks
        - More needed?
    - statistics
        - times visited
        - times voted difficulty
    
"""

class Card:
    def __init__(self, front: str, back: str):
        self.front = front
        self.back = back

    @property
    def front(self):
        return self._front

    @front.setter
    def front(self, value: str):
        if not isinstance(value, str):
            raise ValueError(f"front must be of type 'str', got '{type(value)}'")
        self._front = value

    @property
    def back(self):
        return self._back

    @back.setter
    def back(self, value: str):
        if not isinstance(value, str):
            raise ValueError(f"back must be of type 'str', got '{type(value)}'")
        self._back = value


""" ----- Test Cases ----- """
def test_create_card():
    front = "front"
    back = "back"
    card = Card(front, back)
    return card.back == back and card.front == front

def test_create_bad_front():
    front = 123
    back = "back"
    try:
        card = Card(front, back)
    except ValueError as E:
        return str(E) == "front must be of type 'str', got '<class 'int'>'"
    else:
        return False
    
def test_create_bad_back():
    front = "front"
    back = 123
    try:
        card = Card(front, back)
    except ValueError as E:
        return str(E) == "back must be of type 'str', got '<class 'int'>'"
    else:
        return False

""" ----- Run testcases ----- """
if __name__ == '__main__':
    assert(test_create_card())
    assert(test_create_bad_front())
    assert(test_create_bad_back())