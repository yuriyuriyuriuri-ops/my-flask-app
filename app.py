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
            <title>Flaskテスト</title>
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
        mode = request.form.get("mode", "normal")  # ← モード取得
        model = request.form.get("model", "gpt-4o-mini")  # ← モード取得

        if mode == "quiz":
            messages = [
                {"role": "system", "content": """あなたはクイズ作成AIです。ユーザーの入力に応じてクイズを生成してください。
                ユーザーから受け取った文章を元に、文章に関連づいたクイズを生成してください。
                ユーザーが間違えている部分があれば、解説で教えてあげてください。
                Json {/"問題/", /"選択肢/"(1つ から 4つ), /"答え/"(1つ), /"解説/"} のデータを作って出力してください。
                ユーザーの文章:/"
                """},
                {"role": "user", "content": user_text}
            ]
        else:
            messages = [
                {"role": "user", "content": user_text}
            ]


        responseGPT = client.chat.completions.create(
            model=model,
            messages=messages
        )

        ai_reply = responseGPT.choices[0].message.content

        return f"""
            <title>FlaskChatGPTテスト</title>
            <h1>デバッグ用 ChatGPT <font color="cyan">gpt</font></h1>
            <form method="POST">
                <select name="model">
                    <option value="gpt-4o-mini" {"selected" if model=="gpt-4o-mini" else ""}>gpt-4o-mini</option>
                    <option value="gpt-4" {"selected" if model=="gpt-4" else ""}>gpt-4</option>
                    <option value="gpt-4o" {"selected" if model=="gpt-4o" else ""}>gpt-4o</option>
                </select>

                <label><input type="radio" name="mode" value="normal" {"checked" if mode=="normal" else ""}> 通常モード</label>
                <label><input type="radio" name="mode" value="quiz" {"checked" if mode=="quiz" else ""}> クイズモード</label><br><br>

                <textarea name="text" placeholder="メッセージを入力" style="width:300px;" rows="4" cols="50">{user_text}</textarea>

                <button type="submit" style="font-size:20px; padding:10px 20px;">送信</button>
            </form>

            <p><b>あなた:</b><span style="font-size:15px;">{user_text}</span></p>
            <p><b>AI:</b></p><pre style="color:navy; font-size:15px;">{ai_reply}</pre>

            <p><font color="green">このChatGPTは記憶を行っていません。</font></p>
            <p><font color="blue">クイズはJSON形式で返却されます。</font></p>

            <p><a href="/chat">リセットする</a></p>
            <form action="https://my-flask-app-production-56cf.up.railway.app">
            <button type="submit" style="font-size:20px; padding:10px 20px;">ホームへ戻る</button>
            </form>
        """

    # GET のとき（最初の画面）
    return """
        <title>FlaskChatGPTテスト</title>
        <h1>デバッグ用 ChatGPT <font color="cyan">gpt</font></h1>
        <form method="POST">
            <select name="model">
                <option value="gpt-4o-mini" {"selected" if model=="gpt-4o-mini" else ""}>gpt-4o-mini</option>
                <option value="gpt-4" {"selected" if model=="gpt-4" else ""}>gpt-4</option>
                <option value="gpt-4o" {"selected" if model=="gpt-4o" else ""}>gpt-4o</option>
            </select>

            <label><input type="radio" name="mode" value="normal" checked> 通常モード</label>
            <label><input type="radio" name="mode" value="quiz"> クイズモード</label><br><br>

            <textarea name="text" placeholder="メッセージを入力" style="width:300px;" rows="4" cols="50"></textarea>

            <button type="submit" style="font-size:20px; padding:10px 20px;">送信</button>
        </form>
        <p><font color="green">このChatGPTは記憶を行っていません。</font></p>
        <p><font color="blue">クイズはJSON形式で返却されます。</font></p>
        <form action="https://my-flask-app-production-56cf.up.railway.app">
        <button type="submit" style="font-size:20px; padding:10px 20px;">ホームへ戻る</button>
        </form>
    """