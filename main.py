import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from tkinter import Tk
from gui.interface import BriscolaGUI


# 1. Inizializza e carica il modello
model = SimpleMLP()
model.load_state_dict(torch.load("ai/models/trainer_model.pt"))
model.eval()

# 2. Crea il giocatore con modello
model_player = ModelPlayer(model=model, name="Trainer_AI")

