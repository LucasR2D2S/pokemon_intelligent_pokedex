import React from "react";
import PokedexPage from "./pages/PokedexPage";

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <h1 className="text-4xl text-center font-bold py-4">Pokédex Inteligente</h1>
      <PokedexPage />
    </div>
  );
}

export default App;
// This code defines the main App component for a React application that displays a Pokédex page.
// It imports the PokedexPage component and renders it within a div that has a minimum height and a background color.
// The page includes a title "Pokédex Inteligente" styled with Tailwind CSS classes for text size, alignment, and font weight.