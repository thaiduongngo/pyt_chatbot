import torch
import numpy as np

import services.dao.dao as dao
from services.common.gi import name, age
from services.modeling import BotNN, vectorize_text, file_path
from services.nlp import UNK, lem

accept_min_proba = 0.7
state_data = torch.load(file_path)
input_size = state_data["input_size"]
hidden_size = state_data["hidden_size"]
output_size = state_data["output_size"]
classes = state_data["classes"]
vocabulary = state_data["vocabulary"]

model = BotNN(input_size, hidden_size, output_size)
model.load_state_dict(state_data["model_state"])
model.eval()


def get_unknown_response():
    array = dao.load_unknown_responses()
    i = torch.randint(1, len(array), (1,))[0]
    return array[i]


def get_response(ctx):
    def ev(x):
        return x.replace("{name}", name).replace("{age}", age())

    if ctx == UNK:
        return get_unknown_response()
    else:
        responses = dao.responses_from_ctx(ctx)
        i = np.random.randint(0, len(responses))
        return ev(responses[i]["res"])


def chat(text_message: str, verbose: int = 1):
    x = [vectorize_text(lem(text_message.lower()), vocabulary)]
    x = torch.as_tensor(x, dtype=torch.float32)
    y = model(x)
    _, max_i = torch.max(y, dim=1)
    max_i = max_i[0].item()
    proba = torch.softmax(y, dim=1)[0]
    max_proba = float(proba[max_i].item())
    ctx = classes[max_i]
    org_ctx = ctx

    if max_proba >= accept_min_proba:
        response = get_response(ctx)
    else:
        response = get_unknown_response()
        ctx = UNK

    if verbose > 0:
        return {"response": response, "context": ctx, "origin_context": org_ctx, "probability": max_proba}
    else:
        return {"response": response, "context": ctx, "origin_context": org_ctx}


if __name__ == "__main__":
    print(chat("Hello there"))
    print(chat("notinvocabulary somethingdoesnotexist"))
