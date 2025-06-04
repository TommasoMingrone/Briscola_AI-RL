from game.cards import Deck, Card, Suit
from game.player import Player
import random

class BriscolaGame:
    def __init__(self, player1: Player, player2: Player):
        self.deck = Deck()
        self.players = [player1, player2]
        self.scores = {player1.name: 0, player2.name: 0}
        self.starting_player_index = random.choice([0,1])

        # Draw the briscola card and set the trump suit
        self.briscola_card = self.deck.draw()
        self.briscola_suit = self.briscola_card.suit
        self.deck.cards.insert(0, self.briscola_card)  # Put it at the bottom

        # Deal initial hands (3 cards each)
        for _ in range(3):
            for player in self.players:
                player.receive_card(self.deck.draw())

    def play_turn(self, first_player_index: int) -> int:
        """Plays a single turn of the game, where each player plays one card."""
        p1 = self.players[self.starting_player_index]
        p2 = self.players[1 - self.starting_player_index]

        # Show hands (for debug or console version)
        print(f"{p1.name}'s hand: {p1.show_hand()}")
        print(f"{p2.name}'s hand: {p2.show_hand()}")

        # Each player plays a card
        card1 = p1.play_card()
        card2 = p2.play_card()


        print(f"{p1.name} plays {card1}")
        print(f"{p2.name} plays {card2}")

        # Determine who wins the trick
        winner = self.determine_trick_winner(p1, card1, p2, card2)
        self.scores[winner.name] += card1.points() + card2.points()

        print(f"{winner.name} wins the trick.\n")

        # Update starting player for the next turn
        self.starting_player_index = self.players.index(winner)

        # Each player draws a new card (winner draws first)
        if not self.deck.is_empty():
            winner.receive_card(self.deck.draw())
            loser = p1 if winner == p2 else p2
            loser.receive_card(self.deck.draw())

        return self.starting_player_index

    def determine_trick_winner(self, p1: Player, c1: Card, p2: Player, c2: Card) -> Player:
        # Same suit → it wins the one with higher value
        if c1.suit == c2.suit:
            return p1 if c1.value > c2.value else p2
        
        # One card is briscola → it wins
        if c1.suit == self.briscola_suit and c2.suit != self.briscola_suit:
            return p1
        if c2.suit == self.briscola_suit and c1.suit != self.briscola_suit:
            return p2

        # No briscola cards played and different suits → no one wins
        return self.players[self.starting_player_index]


    def play_game(self):
        """Plays the entire game until the players run out of cards."""
        current_player_index = 0
        while self.players[0].has_cards():
            current_player_index = self.play_turn(current_player_index)

        # Final result
        print("\n=== GAME OVER ===")
        for name, score in self.scores.items():
            print(f"{name}: {score} points")
        winner = max(self.scores, key=self.scores.get)
        print(f"Winner: {winner}")
