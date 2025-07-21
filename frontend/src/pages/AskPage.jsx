import React, { useState, useRef, useEffect } from "react";
import axios from "axios";

export default function AskPage() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [sprites, setSprites] = useState([]);
  const inputRef = useRef(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, [answer, loading]);

  const handleAsk = async () => {
    if (!question.trim()) return;
    setLoading(true);
    setAnswer("");
    setSprites([]);
    try {
      const res = await axios.post("http://localhost:8000/ask", { question });
      setAnswer(res.data.answer);
      setSprites(res.data.sprites || []);
    } catch {
      setAnswer("Erro ao consultar a Pokédex. Tente novamente.");
    } finally {
      setLoading(false);
      setQuestion("");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-700 flex items-center justify-center p-6 font-sans">
      <div className="bg-gray-800 rounded-3xl shadow-xl max-w-md w-full border-4 border-red-600 relative p-6 flex flex-col">
        {/* Top Bar - estilo Pokédex */}
        <div className="flex justify-between items-center mb-4">
          <div className="w-14 h-6 bg-red-600 rounded-lg shadow-inner"></div>
          <div className="text-red-400 font-mono font-semibold tracking-wide text-lg">
            Pokédex AI
          </div>
          <div className="w-14 h-6 bg-red-600 rounded-lg shadow-inner"></div>
        </div>

        {/* Display da resposta */}
        <div
          className="flex-1 bg-gray-900 rounded-xl p-4 text-gray-200 text-sm leading-relaxed select-text"
          style={{ minHeight: "180px", whiteSpace: "pre-wrap" }}
        >
          {loading ? (
            <div className="text-red-500 font-bold animate-pulse text-center">
              Consultando a Pokédex...
            </div>
          ) : answer ? (
            <>
              <p>{answer}</p>
              {sprites.length > 0 && (
                <div className="flex justify-center gap-3 mt-4">
                  {sprites.map((url, i) => (
                    <img
                      key={i}
                      src={url}
                      alt={`Pokémon ${i + 1}`}
                      className="w-20 h-20 drop-shadow-lg"
                    />
                  ))}
                </div>
              )}
            </>
          ) : (
            <p className="text-gray-500 italic text-center">
              Pergunte algo sobre Pokémon!
            </p>
          )}
        </div>

        {/* Barra de status / luzes estilo Pokédex */}
        <div className="flex justify-center gap-3 mt-5">
          <span className="w-4 h-4 bg-red-600 rounded-full animate-pulse shadow-sm"></span>
          <span className="w-4 h-4 bg-yellow-400 rounded-full shadow-sm"></span>
          <span className="w-4 h-4 bg-green-500 rounded-full shadow-sm"></span>
        </div>

        {/* Input e botão */}
        <div className="mt-6 flex gap-3">
          <input
            ref={inputRef}
            type="text"
            placeholder="Digite sua pergunta..."
            className="flex-1 rounded-lg px-4 py-2 bg-gray-700 border border-gray-600 text-gray-200 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-red-600 transition"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleAsk()}
            disabled={loading}
          />
          <button
            onClick={handleAsk}
            disabled={loading}
            className="bg-red-600 hover:bg-red-700 disabled:opacity-50 px-5 rounded-lg text-white font-semibold transition"
          >
            {loading ? "Carregando..." : "Perguntar"}
          </button>
        </div>
      </div>
    </div>
  );
}
