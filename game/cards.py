import random
from enum import Enum

class Suit(Enum):
    BASTONI = "Bastoni"
    COPPE = "Coppe"
    DENARI = "Denari"
    SPADE = "Spade"

# Points associated with each card value
CARD_POINTS = {
    1: 11,  # Asso
    3: 10,
    10: 4,
    9: 3,
    8: 2,
    # 2, 4, 5, 6, 7 → 0 points
}

class Card:
    def __init__(self, value: int, suit: Suit):
        self.value = value  # From 1 to 10
        self.suit = suit

    def points(self) -> int: # Calculate points for the card based on its value
        return CARD_POINTS.get(self.value, 0)

    def __repr__(self): # String representation of the card
        return f"{self.value} di {self.suit.value}"

    def __eq__(self, other): # Check equality of two cards
        return self.value == other.value and self.suit == other.suit

class Deck:
    def __init__(self):
        self.cards = [Card(value, suit) for suit in Suit for value in range(1, 11)]
        random.shuffle(self.cards)

    def draw(self) -> Card: # Draw a card from the deck
        if self.cards:
            return self.cards.pop()
        return None

    def is_empty(self) -> bool: # Check if the deck is empty
        return len(self.cards) == 0

    def __len__(self): # Return the number of cards in the deck
        return len(self.cards)

