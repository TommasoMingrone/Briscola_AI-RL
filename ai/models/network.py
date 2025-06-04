import torch
import torch.nn as nn
import torch.nn.functional as F

class CNNBriscolaModel(nn.Module):
    def __init__(self, input_len=27, num_actions=3):
        super(CNNBriscolaModel, self).__init__()
        self.conv1 = nn.Conv1d(in_channels=1, out_channels=16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv1d(in_channels=16, out_channels=32, kernel_size=3, padding=1)
        self.pool = nn.AdaptiveMaxPool1d(1)  # Reduce temporal dimension to 1
        self.fc = nn.Linear(32, num_actions)

    def forward(self, x):
        # x shape: (batch, 27)
        x = x.unsqueeze(1)  # (batch, 1, 27)
        x = F.relu(self.conv1(x))  # (batch, 16, 27)
        x = F.relu(self.conv2(x))  # (batch, 32, 27)
        x = self.pool(x)           # (batch, 32, 1)
        x = x.squeeze(2)           # (batch, 32)
        x = self.fc(x)             # (batch, num_actions)
        return x


