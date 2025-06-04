import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from game.cards import Deck
from game.player import Player
from game.briscola import BriscolaGame
from ai.agents.rule_based import RuleBasedPlayer
from ai.agents.model_player import ModelPlayer
from ai.models.network import CNNBriscolaModel
import torch


class BriscolaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Briscola AI vs RL (Observer Mode)")

        self.deck = Deck()

        # Load model for ModelPlayer
        model = CNNBriscolaModel()
        model.load_state_dict(torch.load("ai/models/trainer_model.pt"))
        model.eval()

        # Define players
        self.player1 = RuleBasedPlayer("RL_Agent")  # placeholder for RL agent
        self.player2 = ModelPlayer(model=model, name="Model_AI")

        self.game = BriscolaGame(self.player1, self.player2)
        self.current_index = self.game.starting_player_index

        # Layout
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=10, pady=10)

        self.score_frame = tk.Frame(root)
        self.score_frame.pack(pady=5)

        self.score_label_rl = tk.Label(self.score_frame, text="", font=("Arial", 12))
        self.score_label_rl.grid(row=0, column=0, padx=20)

        self.score_label_ai = tk.Label(self.score_frame, text="", font=("Arial", 12))
        self.score_label_ai.grid(row=0, column=1, padx=20)

        self.hand_rl = tk.Label(self.main_frame, text="", font=("Courier", 12), anchor="w", justify="left")
        self.hand_rl.grid(row=0, column=0, padx=10)

        self.play_area = tk.Label(self.main_frame, text="", font=("Arial", 16), width=40)
        self.play_area.grid(row=0, column=1, padx=10)

        self.hand_ai = tk.Label(self.main_frame, text="", font=("Courier", 12), anchor="e", justify="right")
        self.hand_ai.grid(row=0, column=2, padx=10)

        self.status_label = tk.Label(root, text="", font=("Arial", 12))
        self.status_label.pack(pady=5)

        self.card1 = None
        self.card2 = None
        self.p1 = None
        self.p2 = None

        # Start the game
        self.root.after(2500, self.play_phase_1)

    def play_phase_1(self):
        if not self.player1.has_cards():
            self.end_game()
            return

        self.p1 = self.game.players[self.game.starting_player_index]
        self.p2 = self.game.players[1 - self.game.starting_player_index]

        self.card1 = self.p1.play_card()
        self.play_area.config(text=f"{self.p1.name} plays: {self.card1}")

        self.update_hand_display()
        self.root.after(2500, self.play_phase_2)

    def play_phase_2(self):
        self.card2 = self.p2.play_card()
        current = self.play_area.cget("text")
        self.play_area.config(text=current + f"\n{self.p2.name} plays: {self.card2}")

        self.update_hand_display()
        self.root.after(2000, self.play_phase_3)

    def play_phase_3(self):
        winner = self.game.determine_trick_winner(self.p1, self.card1, self.p2, self.card2)
        points = self.card1.points() + self.card2.points()
        self.game.scores[winner.name] += points
        self.game.starting_player_index = self.game.players.index(winner)

        if not self.deck.is_empty():
            winner.receive_card(self.deck.draw())
            loser = self.p1 if winner == self.p2 else self.p2
            loser.receive_card(self.deck.draw())

        self.status_label.config(
            text=f"{winner.name} wins the trick (+{points} pts) | Briscola: {self.game.briscola_suit.value}"
        )

        self.update_hand_display()
        self.update_score_display()
        self.root.after(1500, self.play_phase_1)

    def update_hand_display(self):
        self.hand_rl.config(text="\n".join(f"{i+1}) {card}" for i, card in enumerate(self.player1.hand)))
        self.hand_ai.config(text="\n".join(f"{i+1}) {card}" for i, card in enumerate(self.player2.hand)))

    def update_score_display(self):
        self.score_label_rl.config(
            text=f"{self.player1.name} score: {self.game.scores[self.player1.name]}"
        )
        self.score_label_ai.config(
            text=f"{self.player2.name} score: {self.game.scores[self.player2.name]}"
        )

    def end_game(self):
        final_text = "=== GAME OVER ===\n"
        for name, score in self.game.scores.items():
            final_text += f"{name}: {score} pts\n"
        winner = max(self.game.scores, key=self.game.scores.get)
        final_text += f"Winner: {winner}"
        self.play_area.config(text=final_text)
        self.status_label.config(text="")
