import pytest
import asyncio
from typing import AsyncGenerator, Generator
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
    acho=False
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)

@pytest.fixture
def mock_data():
    return {
        'key1': 'value1',
        'key2': 'value2'
    }

@pytest.fixture(scope='module')
def setup_database():
    # Setup code for database
    yield
    # Teardown code for database

@pytest.fixture
def client():
    from myapp import create_app
    app = create_app()
    with app.test_client() as client:
        yield client