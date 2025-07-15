import React, { useState } from "react";
import axios from "axios";

const AskPage = () => {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAsk = async () => {
    if (!question.trim()) {
      setError("Por favor, digite uma pergunta.");
      return;
    }

    setLoading(true);
    setAnswer("");
    setError("");

    try {
      const response = await axios.post("http://localhost:8000/ask", {
        question: question.trim(),
      });
      setAnswer(response.data.answer || "Sem resposta gerada.");
    } catch (error) {
      console.error("Erro ao consultar assistente:", error);
      setError("Erro ao obter resposta do assistente.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Pergunte à Pokédex Inteligente</h2>

      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        className="w-full p-2 border rounded mb-4"
        rows={4}
        placeholder="Ex: Qual o melhor Pokémon tipo água da geração 2?"
      />

      <button
        onClick={handleAsk}
        disabled={loading}
        className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded disabled:opacity-50"
      >
        {loading ? "Consultando..." : "Perguntar"}
      </button>

      {error && (
        <div className="mt-4 text-red-600 font-semibold">{error}</div>
      )}

      {answer && !error && (
        <div className="mt-6 p-4 bg-gray-100 rounded shadow">
          <h3 className="font-semibold mb-2">Resposta:</h3>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
};

export default AskPage;

// This code defines a React component for a page where users can ask questions to the Pokédex Intelligent assistant.
// It includes a text area for inputting questions, a button to submit the question, and a section to display the answer.
// The component uses Axios to send a POST request to the backend endpoint `/ask` with the user's question.
// The response from the backend is displayed below the input area.
// The component also handles errors by logging them to the console and displaying an error message if the request fails.