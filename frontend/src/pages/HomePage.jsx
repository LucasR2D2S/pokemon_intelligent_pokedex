import React, { useState } from 'react';
import axios from 'axios';

const HomePage = () => {
  const [favoritePokemon, setFavoritePokemon] = useState('');
  const [favoriteType, setFavoriteType] = useState('');
  const [teamPurpose, setTeamPurpose] = useState('');
  const [team, setTeam] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setTeam([]);

    try {
      const response = await axios.post('http://localhost:8000/generate-team/', {
        favorite_pokemon: favoritePokemon,
        favorite_type: favoriteType,
        team_purpose: teamPurpose,
      });

      const teamData = response.data.team;
      const names = teamData.map(p => p.name);

      const pokemonsResponse = await axios.get('http://localhost:8000/pokemon/by-names', {
        params: { names }
      });

      setTeam(pokemonsResponse.data);
    } catch (error) {
      console.error("Erro ao gerar time:", error);
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-yellow-100 to-pink-100 py-10 px-4">
      <div className="max-w-3xl mx-auto bg-white shadow-xl rounded-xl p-6">
        <h1 className="text-3xl font-bold text-center mb-6 text-red-600">🧠 Pokédex Inteligente</h1>

        <form onSubmit={handleSubmit} className="grid grid-cols-1 gap-4 md:grid-cols-3">
          <input
            type="text"
            placeholder="Pokémon favorito"
            value={favoritePokemon}
            onChange={(e) => setFavoritePokemon(e.target.value)}
            className="border border-gray-300 p-2 rounded-lg"
          />
          <input
            type="text"
            placeholder="Tipo favorito"
            value={favoriteType}
            onChange={(e) => setFavoriteType(e.target.value)}
            className="border border-gray-300 p-2 rounded-lg"
          />
          <select
            value={teamPurpose}
            onChange={(e) => setTeamPurpose(e.target.value)}
            className="border border-gray-300 p-2 rounded-lg"
          >
            <option value="">Objetivo</option>
            <option value="fun">Diversão</option>
            <option value="competitive">Competitivo</option>
          </select>

          <button
            type="submit"
            className="col-span-1 md:col-span-3 bg-red-500 hover:bg-red-600 text-white py-2 px-4 rounded-lg transition"
          >
            {loading ? "Gerando Time..." : "Gerar Time"}
          </button>
        </form>

        {team.length > 0 && (
          <div className="mt-10 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
            {team.map((pokemon) => (
              <div
                key={pokemon.id || pokemon.name}
                className="bg-gray-100 p-4 rounded-lg shadow-md text-center"
              >
                <img src={pokemon.image_url} alt={pokemon.name} className="w-24 h-24 mx-auto" />
                <h3 className="text-xl font-semibold mt-2">{pokemon.name}</h3>
                <p><strong>Tipo:</strong> {pokemon.type}</p>
                <p><strong>HP:</strong> {pokemon.hp}</p>
                <p><strong>Ataque:</strong> {pokemon.attack}</p>
                <p><strong>Defesa:</strong> {pokemon.defense}</p>
                <p><strong>Velocidade:</strong> {pokemon.speed}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default HomePage;
// This code defines a HomePage component that allows users to generate a Pokémon team based on their preferences.
// It includes a form for users to input their favorite Pokémon, favorite type, and the purpose of the team (fun or competitive).
// Upon submission, it sends a request to a backend API to generate a team and fetches the details of the Pokémon in that team.
// The generated team is displayed in a grid layout with each Pokémon's image, name, type, and stats. 
// The component uses React hooks for state management and Axios for making HTTP requests.  