import pytest
from fastapi.testclient import TestClient
from backend.main import app

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