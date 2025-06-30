import React, { useEffect, useState } from 'react';
import axios from 'axios';

const PokedexPage = () => {
  const [pokemons, setPokemons] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:8000/pokemon/")
      .then((res) => setPokemons(res.data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div className="p-4 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      {pokemons.map(pokemon => (
        <div key={pokemon.id} className="bg-white rounded-2xl shadow-md p-4 text-center">
          <img src={pokemon.image_url} alt={pokemon.name} className="w-32 mx-auto" />
          <h2 className="text-xl font-bold">{pokemon.name}</h2>
          <p><strong>Tipo:</strong> {pokemon.type}</p>
          <p><strong>HP:</strong> {pokemon.hp}</p>
          <p><strong>Ataque:</strong> {pokemon.attack}</p>
          <p><strong>Defesa:</strong> {pokemon.defense}</p>
          <p><strong>Velocidade:</strong> {pokemon.speed}</p>
        </div>
      ))}
    </div>
  );
};

export default PokedexPage;
// This code defines a PokedexPage component that fetches Pokémon data from a backend API and displays it in a grid layout.
// Each Pokémon is displayed with its image, name, type, and stats like HP, attack, defense, and speed.
// The component uses React hooks for state management and side effects, and Axios for making HTTP requests.