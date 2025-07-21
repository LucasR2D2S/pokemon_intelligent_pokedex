import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import HomePage from './pages/HomePage.jsx';
import AskPage from './pages/AskPage.jsx';

export default function App() {
  return (
    <div className="min-h-screen bg-slate-100 p-4">
      <nav className="mb-4 flex gap-4 text-blue-600">
        <Link to="/">Início</Link>
        <Link to="/ask">Perguntar</Link>
      </nav>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/ask" element={<AskPage />} />
      </Routes>
    </div>
  );
}

// This code defines the main App component for a React application that displays a Pokédex page.
// It imports the PokedexPage component and renders it within a div that has a minimum height and a background color.
// The page includes a title "Pokédex Inteligente" styled with Tailwind CSS classes for text size, alignment, and font weight.