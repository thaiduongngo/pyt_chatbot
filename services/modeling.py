import os
from datetime import datetime

import numpy as np
import torch.nn
import torch.nn as nn
from torch.utils.data import Dataset

from services.common.gi import home_path

epoch_step = 100
file_path = os.path.join(home_path, "models", "state_head.pth")
archive_path = os.path.join(home_path, "models", f"state_{datetime.now().strftime('%Y%m%d%H%M%S')}.pth")


class XyDataset(Dataset):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.n_samples = len(self.x)

    def __getitem__(self, index):
        return self.x[index], self.y[index]

    def __len__(self):
        return self.n_samples


class BotNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(BotNN, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size, output_size)
        self.activation = nn.ReLU()

    def forward(self, x):
        out = self.l1(x)
        out = self.activation(out)
        out = self.l2(out)
        out = self.activation(out)
        out = self.l3(out)
        return out


def to_device():
    return torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")


def vectorize_text(x: [str], vocabulary: [str]):
    vt_size = len(vocabulary)
    vt = list(np.zeros(vt_size, dtype=np.float32))
    for i, w in enumerate(vocabulary):
        if w in x:
            vt[i] += 1.0
    return vt


def vectorize(x: [[str]], vocabulary: [str]):
    vt_list = []
    for words in x:
        vt_list.append(vectorize_text(words, vocabulary))
    return vt_list


def train_model(model: nn.Module, data_loader, epochs, learning_rate):
    print("---BEGIN---")
    device = to_device()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    criterion = nn.CrossEntropyLoss()

    for epoch in range(epochs):
        for (x, y) in data_loader:
            x = x.to(device)
            y = y.to(device)

            # forward
            out = model(x)
            loss = criterion(out, y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        if (epoch + 1) % epoch_step == 0:
            print(f"epoch {epoch + 1}/{epochs}, loss={loss.item():.5f}")

    print(f"Completed, loss={loss.item():.5f}")
    print("---END---")
    return model
