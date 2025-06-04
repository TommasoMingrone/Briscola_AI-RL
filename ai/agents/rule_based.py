import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from game.player import Player

class RuleBasedPlayer(Player):
    def play_card(self):
        if not self.hand:
            return None
        self.original_hand = self.hand.copy()
        # Simple strategy: play lowest point card
        lowest = min(self.hand, key=lambda c: c.points())
        self.hand.remove(lowest)
        return lowest

