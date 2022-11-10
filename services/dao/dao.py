import json

from pymongo import MongoClient

from services.common.gi import lang, home_path

db_host = "localhost"
db_port = 27017
db_name = "train"
db_username = "app"
db_password = "app"
prefix = lang.lower()


def connect():
    out_client = MongoClient(host=db_host, port=db_port)
    out_db = out_client[db_name]
    out_db.authenticate(db_username, db_password)
    return out_client, out_db


def instantiate_data():
    client, db = connect()
    dataset = json.loads(open(f"{home_path}data/{lang}/data.json").read())
    # Instantiate collection
    collection_req = db[f"{lang.lower()}_requests"]
    collection_res = db[f"{lang.lower()}_responses"]
    collection_req.drop()
    collection_res.drop()

    for data in dataset["data"]:
        for req in data["req"]:
            collection_req.insert_one({"req": req, "ctx": data["ctx"]})
        for res in data["res"]:
            collection_res.insert_one({"res": res, "ctx": data["ctx"]})
    client.close()


def instantiate_stopwords():
    client, db = connect()
    dataset = json.loads(open(f"{home_path}data/{lang}/stopwords.json").read())
    collection = db[f"{prefix}_stopwords"]
    collection.drop()
    collection = db[f"{prefix}_stopwords"]
    collection.insert_one(dataset)


def instantiate_unknown_responses():
    client, db = connect()
    dataset = json.loads(
        open(f"{home_path}data/{lang}/unknown-res.json").read())
    collection = db[f"{prefix}_unknown_responses"]
    collection.drop()
    collection = db[f"{prefix}_unknown_responses"]
    collection.insert_one(dataset)
    client.close()


def load_requests():
    client, db = connect()
    collection = db[f"{prefix}_requests"]
    dataset_curs = collection.find({}, {"_id": 0})
    dataset = list(dataset_curs)
    client.close()
    return dataset


def load_responses():
    client, db = connect()
    collection = db[f"{prefix}_responses"]
    dataset_curs = collection.find({}, {"_id": 0})
    dataset = list(dataset_curs)
    client.close()
    return dataset

def responses_from_ctx(ctx):
    client, db = connect()
    collection = db[f"{prefix}_responses"]
    dataset_curs = collection.find({"ctx": ctx}, {"_id": 0, "ctx": 0})
    dataset = list(dataset_curs)
    client.close()
    return dataset

def load_stopwords():
    client, db = connect()
    collection = db[f"{prefix}_stopwords"]
    dataset = collection.find_one({}, {'_id': 0, 'data': 1})
    dataset = dataset["data"]
    client.close()
    return dataset


def load_unknown_responses():
    client, db = connect()
    collection = db[f"{prefix}_unknown_responses"]
    dataset = collection.find_one({}, {'_id': 0, 'data': 1})
    dataset = dataset["data"]
    client.close()
    return dataset


def save_conversation(dict_conversation):
    client, db = connect()
    collection = db[f"{prefix}_conversations"]
    collection.insert_one(dict_conversation)
    client.close()


def save_vocab(vocab):
    client, db = connect()
    collection = db[f"{prefix}_vocab"]
    collection.drop()
    collection.insert_one({"data": vocab})
    client.close()


def load_vocab():
    client, db = connect()
    collection = db[f"{prefix}_vocab"]
    dataset = collection.find_one({}, {'_id': 0, 'data': 1})
    dataset = dataset["data"]
    client.close()
    return dataset

