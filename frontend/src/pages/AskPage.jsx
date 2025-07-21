import React, { useState } from "react";
import axios from "axios";

function AskPage() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question.trim()) return;

    const newMessage = { type: "question", text: question };
    setMessages((prev) => [...prev, newMessage]);
    setQuestion("");
    setLoading(true);

    try {
      const response = await axios.post("http://localhost:8000/ask", { question });
      setMessages((prev) => [
        ...prev,
        { type: "answer", text: response.data.answer },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { type: "answer", text: "Erro ao consultar a Pokédex." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1 className="title">Pokédex Inteligente</h1>
      <div className="chat-window">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`message ${msg.type === "question" ? "question" : "answer"}`}
          >
            {msg.text}
          </div>
        ))}
        {loading && <p className="loading">Consultando a Pokédex...</p>}
      </div>
      <div className="input-area">
        <input
          type="text"
          placeholder="Digite sua pergunta..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleAsk()}
        />
        <button onClick={handleAsk}>Consultar</button>
      </div>
    </div>
  );
}

export default AskPage;
