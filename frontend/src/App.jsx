import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import AskPage from "./pages/AskPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/ask" element={<AskPage />} />
      </Routes>
    </Router>
  );
}
export default App;
// This code defines the main App component for a React application that displays a Pokédex page.
// It imports the PokedexPage component and renders it within a div that has a minimum height and a background color.
// The page includes a title "Pokédex Inteligente" styled with Tailwind CSS classes for text size, alignment, and font weight.