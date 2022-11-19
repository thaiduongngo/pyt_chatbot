import os

import numpy as np
import torch.optim
from torch.utils.data import DataLoader

from services.dao.dao import load_requests
from services.modeling import vectorize, XyDataset, BotNN, train_model, to_device, file_path, archive_path
from services.nlp import lem, UNK

num_seed = 19
requests = load_requests()

X_train = [[""]]
y_train = [UNK]
vocabulary = []

for req in requests:
    wps = lem(req["req"].lower())
    vocabulary.extend(wps)
    X_train.append(wps)
    y_train.append(req["ctx"])

# Build vocabulary
vocabulary = np.unique(vocabulary)

# Build classes
classes = np.unique(y_train)

X_train = torch.as_tensor(vectorize(X_train, vocabulary), dtype=torch.float32)

y_train = np.array(y_train).reshape(-1, 1)
y_train = y_train == classes
y_train = torch.as_tensor(y_train, dtype=torch.float16)

batch_size = 8
input_size = len(X_train[0])
hidden_size = 8
output_size = len(classes)
learning_rate = 0.001
epochs = 1000

device = to_device()
torch.manual_seed(num_seed)
xy_dataset = XyDataset(x=X_train, y=y_train)
xy_loader = DataLoader(dataset=xy_dataset, batch_size=batch_size, shuffle=True, num_workers=0)

# Create model
model = BotNN(input_size, hidden_size, output_size).to(device=device)

# Train model
model = train_model(model=model, data_loader=xy_loader, epochs=epochs, learning_rate=learning_rate)

# Form state data
state_data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "hidden_size": hidden_size,
    "output_size": output_size,
    "classes": classes,
    "vocabulary": vocabulary
}

try:
    os.rename(file_path, archive_path)
except FileNotFoundError as e:
    print(e)

print("Saving model...")
torch.save(state_data, file_path)
print("Saving done")
