"""ChatGPT API を利用したシンプルなチャットボット (Flask バックエンド)。

- `/`          : チャット画面 (HTML) を返す
- `/api/chat`  : ユーザーのメッセージを受け取り ChatGPT API に問い合わせ、応答を返す
"""

import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from openai import APIError, OpenAI, OpenAIError

load_dotenv()

# 使用するモデル。環境変数で上書き可能。
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# チャットボットの人格・振る舞いを決めるシステムプロンプト。
SYSTEM_PROMPT = os.getenv(
    "SYSTEM_PROMPT",
    "あなたは親切で丁寧な日本語のアシスタントです。簡潔で分かりやすく回答してください。",
)

app = Flask(__name__)

# OpenAI クライアントは遅延生成する。
# こうすることで API キー未設定でもサーバー自体は起動し、
# チャット時に分かりやすいエラーを返せる。
_client = None


def get_client():
    """OpenAI クライアントを取得する (初回のみ生成)。APIキーは環境変数から読み込む。"""
    global _client
    if _client is None:
        _client = OpenAI()
    return _client


@app.route("/")
def index():
    """チャット画面を返す。"""
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """ユーザーのメッセージを ChatGPT API へ送り、応答テキストを返す。

    リクエスト JSON:
        {
          "message": "こんにちは",
          "history": [{"role": "user"|"assistant", "content": "..."}]  # 任意
        }
    レスポンス JSON:
        {"reply": "..."}  または  {"error": "..."}
    """
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    history = data.get("history") or []

    if not message:
        return jsonify({"error": "メッセージが空です。"}), 400

    if not os.getenv("OPENAI_API_KEY"):
        return jsonify({"error": "OPENAI_API_KEY が設定されていません。.env を確認してください。"}), 500

    # システムプロンプト + これまでの会話履歴 + 今回の発言を組み立てる。
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for item in history:
        role = item.get("role")
        content = item.get("content")
        if role in ("user", "assistant") and content:
            messages.append({"role": role, "content": content})
    messages.append({"role": "user", "content": message})

    try:
        completion = get_client().chat.completions.create(
            model=MODEL,
            messages=messages,
        )
        reply = completion.choices[0].message.content
        return jsonify({"reply": reply})
    except APIError as exc:
        # OpenAI 側のエラー (レート制限・認証など)。
        app.logger.exception("OpenAI API error")
        return jsonify({"error": f"ChatGPT API エラー: {exc}"}), 502
    except OpenAIError as exc:
        app.logger.exception("OpenAI client error")
        return jsonify({"error": f"リクエストに失敗しました: {exc}"}), 500


if __name__ == "__main__":
    # 開発用サーバー。本番では gunicorn などを利用する。
    app.run(host="127.0.0.1", port=5001, debug=True)
