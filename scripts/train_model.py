import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import torch
import matplotlib.pyplot as plt
from torch.utils.data import TensorDataset, DataLoader
import pandas as pd
import csv
from ai.models.network import CNNBriscolaModel


# Load dataset
df = pd.read_csv("data/dataset.csv")
X = df.iloc[:, :-1].values
y = df.iloc[:, -1].values

X_tensor = torch.tensor(X, dtype=torch.float32)
y_tensor = torch.tensor(y, dtype=torch.long)

dataset = TensorDataset(X_tensor, y_tensor)
loader = DataLoader(dataset, batch_size=32, shuffle=True)

# Model
model = CNNBriscolaModel()
# Optimizer & scheduler
optimizer = torch.optim.Adam(model.parameters(), lr=1e-2)  # LR iniziale più alto
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)

loss_fn = torch.nn.CrossEntropyLoss()

# Training loop
epochs = 30
loss_history = []
accuracy_history = []

with open("data/training_log.csv", "w", newline="") as log_file:
    writer = csv.writer(log_file)
    writer.writerow(["Epoch", "Loss", "Accuracy"])

    for epoch in range(epochs):
        total_loss = 0.0
        correct = 0
        total = 0

        for xb, yb in loader:
            optimizer.zero_grad()
            preds = model(xb)
            loss = loss_fn(preds, yb)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            predicted = torch.argmax(preds, dim=1)
            correct += (predicted == yb).sum().item()
            total += yb.size(0)

        avg_loss = total_loss / len(loader)
        accuracy = correct / total

        loss_history.append(avg_loss)
        accuracy_history.append(accuracy)
        writer.writerow([epoch + 1, avg_loss, accuracy])

        print(f"Epoch {epoch+1} | Loss: {avg_loss:.4f} | Accuracy: {accuracy:.2%}")

        scheduler.step()

# Save model
torch.save(model.state_dict(), "ai/models/trainer_model.pt")

# Plot
fig, ax1 = plt.subplots()

ax1.set_xlabel("Epoch")
ax1.set_ylabel("Loss", color="blue")
ax1.plot(range(1, epochs + 1), loss_history, color="blue", label="Loss")
ax1.tick_params(axis="y", labelcolor="blue")

ax2 = ax1.twinx()
ax2.set_ylabel("Accuracy", color="green")
ax2.plot(range(1, epochs + 1), accuracy_history, color="green", label="Accuracy")
ax2.tick_params(axis="y", labelcolor="green")

plt.title("Training Loss & Accuracy")
fig.tight_layout()
plt.show()
