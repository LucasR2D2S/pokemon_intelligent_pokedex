async function sendQuestion() {
  const question = document.getElementById('question').value;
  const answerDiv = document.getElementById('answer');
  answerDiv.innerHTML = "Consultando...";

  try {
    const response = await fetch("http://localhost:8000/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ question })
    });

    const data = await response.json();
    answerDiv.innerHTML = `<strong>Resposta:</strong><br>${data.answer}`;
  } catch (error) {
    answerDiv.innerHTML = "Erro ao consultar a Pokédex. Verifique a conexão com o servidor.";
    console.error(error);
  }
}
