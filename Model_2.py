# -*- coding: utf-8 -*-
"""P2 (1).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19SElnueuDfZkuITo8L5s5VP4WyQLgPMf
"""

# General libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# Load the CSV data
data = pd.read_csv('/content/AI_ML.csv')
data = data.replace({',': ''}, regex=True)
data = data.apply(pd.to_numeric, errors='coerce')

X = data.iloc[:, 10:13].values
y = data.iloc[:, 13].values

# Normalize the input features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split into train and test sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.08, random_state=42)

mean = scaler.mean_
std = scaler.scale_

print("Mean:", mean)
print("Standard Deviation:", std)

# Convert to PyTorch tensors
X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)

X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)

train_data = TensorDataset(X_train_tensor, y_train_tensor)

# Create a DataLoader for batching
batch_size = 32
train_loader = DataLoader(dataset=train_data, batch_size=batch_size, shuffle=True)

class MLP(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(MLP, self).__init__()

        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.LeakyReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)


    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

# Create the model instance
model = MLP(input_size=3, hidden_size=75, output_size=1)

# Define the loss function for regression
criterion = nn.MSELoss()

# Define the Adam optimizer
optimizer = optim.AdamW(model.parameters(), lr=0.001, weight_decay=1e-4)

# Training loop
num_epochs = 2500
epoch_losses = []
r2_scores = []
for epoch in range(num_epochs):
    model.train()
    total_loss = 0.0

    for inputs, targets in train_loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    avg_loss = total_loss / len(train_loader)
    epoch_losses.append(avg_loss)

    with torch.no_grad():
        predicted_values = model(inputs)
        r2 = r2_score(targets.cpu().numpy(), predicted_values.cpu().numpy())
        r2_scores.append(r2)

    # Print the loss and R² every 100 epochs for monitoring
    if (epoch + 1) % 100 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {avg_loss:.4f}, R²: {r2:.4f}')

model.eval()

with torch.no_grad():
    predictions = model(X_test_tensor)


criterion = nn.MSELoss()
test_loss = criterion(predictions, y_test_tensor)

print(f'Test MSE Loss: {test_loss.item():.4f}')

# Plot the loss curve
plt.figure(figsize=(10, 6))
plt.plot(range(1, num_epochs + 1), epoch_losses, label='Training Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Epoch vs Loss')
plt.ylim(0, 1)
plt.grid(True)
plt.legend()
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(range(1, num_epochs + 1), r2_scores, label='R² Score', color='green')
plt.xlabel('Epochs')
plt.ylabel('R² Score')
plt.ylim(0.9, 1)
plt.title('R² Score Over Epochs')
plt.grid(True)
plt.legend()
plt.show()

# Calculate R² score (Goodness of Fit)
y_test_mean = y_test_tensor.mean()
total_sum_of_squares = ((y_test_tensor - y_test_mean) ** 2).sum()
residual_sum_of_squares = ((y_test_tensor - predictions) ** 2).sum()

r2_score = 1 - (residual_sum_of_squares / total_sum_of_squares)
print(f'R² Score: {r2_score:.4f}')

# Convert the tensors to numpy arrays
y_test_np = y_test_tensor.numpy()
y_pred_np = predictions.numpy()

# Create a DataFrame to display both true and predicted values
df = pd.DataFrame({
    'True Values': y_test_np.flatten(),
    'Predicted Values': y_pred_np.flatten()
})

# Convert the tensors to numpy arrays
y_test_np = y_test_tensor.numpy()
y_pred_np = predictions.numpy()

# Create a DataFrame to display both true and predicted values
df = pd.DataFrame({
    'True Values': y_test_np.flatten(),
    'Predicted Values': y_pred_np.flatten()
})

print(df[:])

true_values = df['True Values']
predicted_values = df['Predicted Values']


plt.figure(figsize=(8, 6))
plt.scatter(true_values, predicted_values, color='blue', alpha=0.5, label='Predicted vs True')

plt.plot([true_values.min(), true_values.max()], [true_values.min(), true_values.max()], color='red', linestyle='--', label='Perfect Prediction')


plt.xlabel('True Values')
plt.ylabel('Predicted Values')
plt.title('True vs Predicted Values')
plt.legend()
plt.show()

resistivity = float(input("Enter resistivity (rho): "))  # User input for resistivity
length = float(input("Enter length (L): "))  # User input for length
width = float(input("Enter width (W): "))  # User input for width

dry_thickness = 13.45

# Calculate rho_naught using the given formula
rho_naught = 25.4 * resistivity

# Calculate rs value
rs = rho_naught / dry_thickness

# Calculate the final result by multiplying by the factor (L / W)
final_result = rs * (length / width)

# Output the final result
print(f"The final result is: {final_result:.4f}")