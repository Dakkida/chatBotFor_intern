const form = document.getElementById("chat-form");
const input = document.getElementById("input");
const sendBtn = document.getElementById("send");
const messagesEl = document.getElementById("messages");

// これまでの会話履歴 (システムプロンプトを除く user/assistant のやり取り)。
const history = [];

/** 画面にメッセージの吹き出しを追加して、その要素を返す。 */
function addMessage(role, text, extraClass = "") {
  const wrap = document.createElement("div");
  wrap.className = `message ${role}`;

  const bubble = document.createElement("div");
  bubble.className = `bubble ${extraClass}`.trim();
  bubble.textContent = text;

  wrap.appendChild(bubble);
  messagesEl.appendChild(wrap);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return wrap;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = input.value.trim();
  if (!message) return;

  // ユーザー発言を表示。
  addMessage("user", message);
  input.value = "";
  input.focus();
  sendBtn.disabled = true;

  // 応答待ちの「入力中」表示。
  const typingEl = addMessage("bot", "入力中…", "typing");

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, history }),
    });
    const data = await res.json();
    typingEl.remove();

    if (!res.ok) {
      addMessage("bot", data.error || "エラーが発生しました。");
      return;
    }

    const reply = data.reply;
    addMessage("bot", reply);

    // 履歴を更新 (次のリクエストで文脈として送る)。
    history.push({ role: "user", content: message });
    history.push({ role: "assistant", content: reply });
  } catch (err) {
    typingEl.remove();
    addMessage("bot", "通信に失敗しました。サーバーが起動しているか確認してください。");
  } finally {
    sendBtn.disabled = false;
  }
});
