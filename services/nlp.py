import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import wordpunct_tokenize

from services.dao import dao

nltk.download('wordnet')
nltk.download('punkt')

UNK = "[UNK]"
stopwords = set(dao.load_stopwords())
wnl = WordNetLemmatizer()


def lem(s: str):
    def process_lem(x):
        w = wnl.lemmatize(x)
        return w

    words = wordpunct_tokenize(s)
    words = [process_lem(word) for word in words if word not in stopwords]
    return words


def build_vocab(vocabulary=None):
    if vocabulary is None:
        vocab = []
        requests = dao.load_requests()
        for req in requests:
            words = lem(req["req"].lower())
            vocab.extend(words)
        vocab = np.unique(vocab)
        dao.save_vocab(list(vocab))
        return vocab
    else:
        dao.save_vocab(vocabulary)
        return vocabulary


def load_vocab():
    vocab = dao.load_vocab()
    return vocab


if __name__ == "__main__":
    pass
