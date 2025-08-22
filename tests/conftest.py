import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Import your app components
from backend.main import app
from backend.database.db import Base, get_db
from backend.database.models import Pokemon
from backend.core.config import settings

TEST_DATABASE_URL = "sqlite:///./test_pokedex.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)

# Funções de configuração dos testes, loop, banco de dados e cliente

@pytest.fixture(scope="session")
def event_loop():
    # Criando instancia default de event loop para testes
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope='function')
def db_session():
    # Criando um db para cada teste, garantindo o isolamento dos dados.
    Base.metadata.create_all(bind=test_engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope="function")
def client(db_session):
    # Cria um cliente de teste com a sessão do banco de dados de teste
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

# Funções criando dados de exemplo para testes

@pytest.fixture
def sample_pokemon_data():
    # Dados de exemplo para um Pokémon
    return {
        "id": 25,
        "name": "Pikachu",
        "types": ["electric"],
        "stats": [35, 55, 40, 50, 50, 90],  # HP, Attack, Defense, Sp.Atk, Sp.Def, Speed
        "generation": "G1",
        "physical_characteristics": "Pikachu is a small, rodent-like Pokemon with yellow fur.",
        "behavior": "Pikachu is known for storing electricity in its cheek pouches.",
        "habitat": "Pikachu can be found in forests and grasslands.",
        "general_description": "This Pokemon has electricity-storing pouches on its cheeks.",
        "full_description": "Pikachu is an Electric-type Pokemon. This Pokemon has electricity-storing pouches on its cheeks. These appear to become electrically charged during the night while Pikachu sleeps."
    }

@pytest.fixture
def sample_pokemon_in_db(db_session, sample_pokemon_data):
    # Cria um Pokémon de exemplo no banco de dados de teste
    pokemon = Pokemon(**sample_pokemon_data)
    db_session.add(pokemon)
    db_session.commit()
    db_session.refresh(pokemon)
    return pokemon

@pytest.fixture
def multiple_pokemon_data():
    # Dados de exemplo para múltiplos Pokémons
    return [
        {
            "id": 4,
            "name": "Charmander",
            "types": ["fire"],
            "stats": [39, 52, 43, 60, 50, 65],
            "generation": "G1",
            "physical_characteristics": "Charmander is a bipedal, reptilian Pokemon with orange skin.",
            "behavior": "Charmander is known for its loyalty to its trainer.",
            "habitat": "Charmander can be found in hot, mountainous areas.",
            "general_description": "Obviously prefers hot places. When it rains, steam is said to spout from the tip of its tail.",
            "full_description": "Charmander is a Fire-type Pokemon. Obviously prefers hot places. When it rains, steam is said to spout from the tip of its tail. The flame at the tip of its tail makes a sound as it burns."
        },
        {
            "id": 1,
            "name": "Bulbasaur",
            "types": ["grass", "poison"],
            "stats": [45, 49, 49, 65, 65, 45],
            "generation": "G1",
            "physical_characteristics": "Bulbasaur is a small, quadruped Pokémon that has blue-green skin with darker blue-green spots.",
            "behavior": "Bulbasaur can be seen napping in bright sunlight.",
            "habitat": "Bulbasaur can be found in grassy areas.",
            "general_description": "A strange seed was planted on its back at birth. The plant sprouts and grows with this Pokémon.",
            "full_description": "Bulbasaur is a Grass/Poison-type Pokémon. A strange seed was planted on its back at birth. The plant sprouts and grows with this Pokémon. It can be seen napping in bright sunlight."
        }
    ]

@pytest.fixture
def multiple_pokemon_in_db(db_session, multiple_pokemon_data):
    # Cria múltiplos Pokémons de exemplo no banco de dados de teste
    pokemons = [Pokemon(**data) for data in multiple_pokemon_data]
    db_session.add_all(pokemons)
    db_session.commit()
    return pokemons

