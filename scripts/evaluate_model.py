import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import torch
from ai.models.network import CNNBriscolaModel
from ai.agents.model_player import ModelPlayer
from ai.agents.rule_based import RuleBasedPlayer
from game.briscola import BriscolaGame

def evaluate(n_games=100):
    model = CNNBriscolaModel()
    model.load_state_dict(torch.load("ai/models/trainer_model.pt"))
    model.eval()

    model_wins = 0
    rule_wins = 0
    draws = 0
    total_model_score = 0
    total_rule_score = 0

    for i in range(n_games):
        model_player = ModelPlayer(model=model, name="Model_AI")
        rule_player = RuleBasedPlayer("Rule_Based")
        game = BriscolaGame(model_player, rule_player)
        game.play_game()

        score_model = game.scores["Model_AI"]
        score_rule = game.scores["Rule_Based"]

        total_model_score += score_model
        total_rule_score += score_rule

        if score_model > score_rule:
            model_wins += 1
        elif score_model < score_rule:
            rule_wins += 1
        else:
            draws += 1

        print(f"Game {i+1}: Model_AI {score_model} vs Rule_Based {score_rule}")

    print("\n=== Evaluation Summary ===")
    print(f"Total games: {n_games}")
    print(f"Model_AI wins: {model_wins} ({model_wins / n_games:.2%})")
    print(f"Rule_Based wins: {rule_wins} ({rule_wins / n_games:.2%})")
    print(f"Draws: {draws}")
    print(f"Average score - Model_AI: {total_model_score / n_games:.2f}")
    print(f"Average score - Rule_Based: {total_rule_score / n_games:.2f}")

if __name__ == "__main__":
    evaluate(n_games=100)
