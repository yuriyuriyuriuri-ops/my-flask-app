from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "こんにちは、これはRenderで動いてるFlaskアプリです！"

@app.route("/a")
def hello():
    return "これは /a ページです。"

# Renderでは gunicorn が起動するので app.run() は不要