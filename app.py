from flask import Flask, request, jsonify
#Flaskのインポートと、リクエスト、JSON関連
import os

from openai import OpenAI
#ChatGPTのインポート

app = Flask(__name__)

client = OpenAI(api_key = os.environ["OPENAI_API_KEY"])
#ChatGPTのキー

@app.route("/")
def home():
    return """
            <style>
            a {
            color: blue; /* 通常時の色 */
            text-decoration: none;
            }

            a:hover {
            color: red; /* ホバー時の色 */
            }
            </style>
            <p>こんにちは、これはFlaskアプリです！</p>
            <h1>FlaskでのWebページ</h1>
                <h2 style="color : orange;">こんにちは</h2>
                <h2><a href="https://my-flask-app-production-56cf.up.railway.app/chat">ChatGPTと会話</a></h2>
                <p><a href="https://my-flask-app-production-56cf.up.railway.app/a">さようなら</a></p>
            """
#デフォルトのサイト

@app.route("/a")
def hello():
    return """
            <style>
            a {
            color: blue; /* 通常時の色 */
            text-decoration: none;
            }

            a:hover {
            color: red; /* ホバー時の色 */
            }
            </style>
            <p>これは /a ページです。</p>
            <h1>FlaskでのWebページ2</h1>
                <h2 style="color : indigo;">さようなら</h2>
                <a><a href="https://my-flask-app-production-56cf.up.railway.app/">こんにちは</a></p>"""
#サブサイト

# -------------------------
# 外部アプリ用 API
# -------------------------

@app.route("/receive", methods=["POST"])
def receive():
    data = request.get_data(as_text=True)
    return jsonify({"received": data + "\n返却されました。"})
#データ返却テスト

@app.route("/receiveGPT", methods=["POST"])
def receiveGPT():
    user_text = request.get_data(as_text=True)

    # ChatGPT に送る
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": user_text}
        ]
    )
#ChatGPTと会話
    ai_reply = response.choices[0].message["content"]

    return jsonify({"reply": ai_reply})

# -------------------------
# デバッグ用 Web UI
# -------------------------
@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_text = request.form.get("text", "")

        responseGPT = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_text}]
        )

        ai_reply = responseGPT.choices[0].message.content

        return f"""
            <h1>デバッグ用 ChatGPT</h1>
            <form method="POST">
                <input type="text" name="text" value="{user_text}" style="width:300px;">
                <button type="submit">送信</button>
            </form>
            <p><b>あなた:</b> {user_text}</p>
            <p><b>AI:</b> {ai_reply}</p>
            <p><a href="/chat">リセット</a></p>
        """

    # GET のとき（最初の画面）
    return """
        <h1>デバッグ用 ChatGPT</h1>
        <form method="POST">
            <input type="text" name="text" placeholder="メッセージを入力" style="width:300px;">
            <button type="submit">送信</button>
        </form>
    """
