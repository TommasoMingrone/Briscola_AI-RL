import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from game.player import Player
import numpy as np
import torch

class ModelPlayer(Player):
    def __init__(self, model, name="Model_AI"):
        super().__init__(name)
        self.model = model

    def encode_state(self):
        # Normalizza per sicurezza
        return torch.tensor([card.value / 10 for card in self.hand] + [0] * (3 - len(self.hand)), dtype=torch.float32)

    def play_card(self):
        if not self.hand:
            return None
        state = self.encode_state().unsqueeze(0)  # shape: (1, input_dim)
        with torch.no_grad():
            output = self.model(state)
            action = torch.argmax(output).item()
        return self.hand.pop(action if action < len(self.hand) else 0)
