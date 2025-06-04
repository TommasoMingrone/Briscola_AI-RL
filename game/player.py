from game.cards import Card
from typing import List

class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand: List[Card] = []

    def receive_card(self, card: Card):
        """Receve a card and add it to the player's hand."""
        if card:
            self.hand.append(card)

    def play_card(self, index: int) -> Card:
        """Play a card from the player's hand at the specified index."""
        if 0 <= index < len(self.hand):
            return self.hand.pop(index)
        raise ValueError("Not a valid index.")

    def show_hand(self) -> str:
        """Show the player's hand with card indices."""
        return ', '.join(f"[{i}] {card}" for i, card in enumerate(self.hand))

    def has_cards(self) -> bool:
        """Check if the player has any cards in hand."""
        return len(self.hand) > 0
