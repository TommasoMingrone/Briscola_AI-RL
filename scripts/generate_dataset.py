import sys
import os
import csv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from game.briscola import BriscolaGame
from ai.agents.rule_based import RuleBasedPlayer
from game.cards import Suit

"""
=====================
Sequential Briscola Dataset Documentation
=====================

Each row in the dataset represents a single training example for the AI agent,
built from a sequence of the last 3 turns seen by the player.

=====================
Feature Description
=====================

Each state is represented by 5 features:
    - v1: value of the first card in hand (integer from 1 to 10)
    - v2: value of the second card in hand (integer from 1 to 10)
    - v3: value of the third card in hand (integer from 1 to 10)
    - briscola: integer encoding of the trump suit
        (0 = Bastoni, 1 = Coppe, 2 = Denari, 3 = Spade)
    - opp: value of the card played by the opponent during this turn (0 if none)

The full input consists of 3 consecutive states:
    s0 → two turns ago
    s1 → previous turn
    s2 → current turn

Total features per row: 3 states × 5 features = 15 values

=====================
Target
=====================

The "action" field is the index of the card played by the agent during the current state (s2):
    - 0 → first card in hand
    - 1 → second card
    - 2 → third card

=====================
Example Row
=====================

s0_v1,s0_v2,s0_v3,s0_briscola,s0_opp,
s1_v1,s1_v2,s1_v3,s1_briscola,s1_opp,
s2_v1,s2_v2,s2_v3,s2_briscola,s2_opp,
action

5,7,8,0,0, 5,7,8,0,0, 5,7,8,0,0, 0

Meaning:
  → Over the last 3 rounds, the player's hand was consistently [5, 7, 8], trump suit was "Bastoni" (0),
    and the opponent hadn't played a card yet.
  → The agent decided to play the first card (index 0) from its current hand.

=====================
Purpose
=====================

This dataset format enables models to learn temporal dependencies across rounds.
It is especially suitable for:
    - 1D Convolutional Neural Networks (CNNs)
    - LSTM / GRU recurrent networks
    - Transformers
    - Flattened input to fully connected MLPs

The goal is to help the model go beyond reactive behavior
by understanding short-term strategies and card dynamics over time.
"""

# Helper: encode a single game state

def encode_card(card):
    """Restituisce [valore, seme] oppure [0, 0] se la carta è None"""
    return [card.value, list(Suit).index(card.suit)] if card else [0, 0]

def encode_state(hand, briscola, opponent_card):
    state = []
    for card in hand:
        state += encode_card(card)
    while len(state) < 6:  # 3 carte x [valore, seme]
        state += [0, 0]
    state += [list(Suit).index(briscola)]  # Briscola come intero
    state += encode_card(opponent_card)    # Carta avversaria (valore, seme)
    return state



# Helper: flatten list of lists
def flatten(sequences):
    return [val for seq in sequences for val in seq]

# Generate sequential dataset
def generate_sequential_data(n_games=1000, save_path="data/dataset.csv", sequence_len=3):
    with open(save_path, "w", newline="") as f:
        writer = csv.writer(f)

        # Header: s0_v1, ..., s2_opp, action
        header = []
        for t in range(sequence_len):  # per s0, s1, s2
            header += [
                f"s{t}_v1", f"s{t}_s1", f"s{t}_v2", f"s{t}_s2", f"s{t}_v3", f"s{t}_s3", f"s{t}_briscola", f"s{t}_opp_v", f"s{t}_opp_s"
            ]
        header += ["action"]

        writer.writerow(header)

        for _ in range(n_games):
            p1 = RuleBasedPlayer("Trainer")
            p2 = RuleBasedPlayer("Opponent")
            game = BriscolaGame(p1, p2)

            memory = {p.name: [] for p in game.players}

            while p1.has_cards():
                for i, player in enumerate(game.players):
                    opponent = game.players[1 - i]
                    opp_card = getattr(opponent, "last_card_played", None)

                    current_state = encode_state(player.hand, game.briscola_suit, opp_card)
                    memory[player.name].append(current_state)

                    if len(memory[player.name]) >= sequence_len:
                        sequence = memory[player.name][-sequence_len:]
                        played_card = player.play_card()
                        try:
                            action_index = player.original_hand.index(played_card)
                        except:
                            action_index = 0

                        writer.writerow(flatten(sequence) + [action_index])
                        player.last_card_played = played_card

if __name__ == "__main__":
    generate_sequential_data(n_games=10000)
    print("Sequential dataset saved to data/dataset.csv")
