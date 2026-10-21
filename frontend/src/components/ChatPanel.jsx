import { useEffect, useRef, useState } from "react";
import { api } from "../api/client";

// POST /analysis/chat only accepts { question } and keeps no history, so to let
// follow-up questions work we fold the last few turns into the question text.
const HISTORY_TURNS = 6;

function buildQuestion(history, question) {
  const recent = history.filter((m) => !m.error).slice(-HISTORY_TURNS);
  if (recent.length === 0) return question;
  const transcript = recent
    .map((m) => `${m.role === "user" ? "User" : "Assistant"}: ${m.text}`)
    .join("\n");
  return `Conversation so far:\n${transcript}\n\nUser: ${question}\n\nReply to the latest user message.`;
}

// The backend may return a bare string or an object like { response: "..." }.
// Accept both so a change in response shape doesn't show up as an empty answer.
function extractText(res) {
  if (typeof res === "string") return res.trim();
  if (res && typeof res === "object") {
    const value = res.response ?? res.answer ?? res.message ?? res.content;
    if (typeof value === "string") return value.trim();
  }
  return "";
}

export default function ChatPanel() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [pending, setPending] = useState(false);
  const logRef = useRef(null);

  useEffect(() => {
    const el = logRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [messages, pending]);

  async function send() {
    const question = input.trim();
    if (!question || pending) return;

    const history = messages;
    setMessages((m) => [...m, { role: "user", text: question }]);
    setInput("");
    setPending(true);

    try {
      const res = await api.chat(buildQuestion(history, question));
      const text = extractText(res);
      setMessages((m) => [
        ...m,
        text
          ? { role: "bot", text }
          : { role: "bot", text: "The assistant sent back an empty answer. Try asking again.", error: true },
      ]);
    } catch (err) {
      setMessages((m) => [...m, { role: "bot", text: err.message, error: true }]);
    } finally {
      setPending(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  }

  return (
    <div className="panel">
      <div className="panel-header">
        <h2>Assistant</h2>
        {messages.length > 0 && (
          <button className="ghost" onClick={() => setMessages([])} disabled={pending}>
            New chat
          </button>
        )}
      </div>

      <div className="chat">
        <div className="chat-log" ref={logRef} aria-live="polite">
          {messages.length === 0 && !pending && (
            <p className="chat-empty">Ask a question to get started. Press Enter to send, Shift+Enter for a new line.</p>
          )}
          {messages.map((m, i) => (
            <div key={i} className={`msg ${m.role === "user" ? "user" : "bot"}${m.error ? " failed" : ""}`}>
              {m.text}
            </div>
          ))}
          {pending && <div className="msg bot pending">Thinking...</div>}
        </div>

        <form
          className="chat-form"
          onSubmit={(e) => {
            e.preventDefault();
            send();
          }}
        >
          <textarea
            rows={2}
            placeholder="Type your question"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            aria-label="Your question"
          />
          <button type="submit" disabled={pending || !input.trim()}>
            Send
          </button>
        </form>
      </div>
    </div>
  );
}
