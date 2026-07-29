# ChatGPT チャットボット (Flask)

ChatGPT API を利用したシンプルなチャットボットです。
Python / Flask のバックエンドと、素の HTML/CSS/JavaScript のフロントエンドで構成しています。

## 機能

- ユーザーからの入力を受け取るチャット画面
- ChatGPT API (OpenAI) へのリクエスト送信
- レスポンスの表示
- 会話履歴を保持したマルチターン対応（文脈を踏まえた応答）

## 構成

```
chatBot_flask/
├── app.py              # Flask バックエンド (ChatGPT API 呼び出し)
├── requirements.txt    # 依存パッケージ
├── .env.example        # 環境変数のサンプル
├── templates/
│   └── index.html      # チャット画面
└── static/
    ├── style.css       # スタイル
    └── script.js       # フロント側ロジック (fetch で API 呼び出し)
```

## セットアップ

1. 依存パッケージをインストール

   ```bash
   cd chatBot_flask
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. 環境変数を設定（`.env.example` をコピーして API キーを記入）

   ```bash
   cp .env.example .env
   # .env を編集し OPENAI_API_KEY を設定
   ```

   OpenAI の API キーは https://platform.openai.com/api-keys から取得できます。

## 起動

```bash
python app.py
```

ブラウザで http://127.0.0.1:5001 を開くとチャット画面が表示されます。

## 技術メモ

- モデルは既定で `gpt-4o-mini`。`.env` の `OPENAI_MODEL` で変更可能。
- 会話履歴はフロント側で保持し、リクエストごとにサーバーへ送信しています。
- 本番運用では開発サーバーではなく gunicorn 等を利用してください。
# chatBotFor_intern
