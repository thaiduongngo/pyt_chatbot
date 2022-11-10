
from flask import Flask, jsonify, request
from markupsafe import escape
from flask_cors import CORS
import requests

from services.chatbot import chat
from services.common.wcrawler import get_weather_info


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/api/chat/<text_message>", methods=['GET'])
def chat_path(text_message: str):
    return chat(text_message=escape(text_message))


@app.route("/api/chat/", methods=['GET'])
def chat_param():
    args = request.args
    text_message = args.get("text_message")
    return chat(text_message=escape(text_message))


@app.route("/api/weather/")
def weather_path():
    return get_weather_info()


@app.route("/api/forex/<pairs>")
def forex_path(pairs: str):
    api_url = f"https://www.freeforexapi.com/api/live?pairs={escape(pairs)}"
    res = requests.get(api_url)
    return jsonify(res.json())


if __name__ == "__main__":
    app.run(debug=True)
