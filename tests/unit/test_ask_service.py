import pytest
from backend.api import ask_routes
@pytest.fixture
def mock_data():
    return {
        'question': 'Qual o pokemon que é um rato amarelo?',
        'answer': 'Pikachu'
    }

def test_ask_service_get_answer(mock_data):
    service = ask_routes()
    answer = service.get_answer(mock_data['question'])
    assert answer == mock_data['answer']

def test_ask_service_invalid_question():
    service = ask_routes()
    answer = service.get_answer('Invalid question?')
    assert answer is None