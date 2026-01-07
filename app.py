from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "こんにちは、これはFlaskアプリです！"

@app.route("/a")
def hello():
    return "これは /a ページです。"