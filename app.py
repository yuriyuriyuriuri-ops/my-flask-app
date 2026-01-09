from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return """こんにちは、これはFlaskアプリです！
            <style>
            a {
            color: blue; /* 通常時の色 */
            text-decoration: none;
            }

            a:hover {
            color: red; /* ホバー時の色 */
            }
            </style>
            <h1>FlaskでのWebページ</h1>
                <h2 style="color : orange;">こんにちは</h2>
                <p><a href="https://my-flask-app-production-bf54.up.railway.app/a">さようなら</a></p>
            """

@app.route("/a")
def hello():
    return """これは /a ページです。
            <style>
            a {
            color: blue; /* 通常時の色 */
            text-decoration: none;
            }

            a:hover {
            color: red; /* ホバー時の色 */
            }
            </style>
            <h1>FlaskでのWebページ2</h1>
                <h2 style="color : indigo;">さようなら</h2>
                <a><a href="https://my-flask-app-production-bf54.up.railway.app/">こんにちは</a></p>"""

app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))