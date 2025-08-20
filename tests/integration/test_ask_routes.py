import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_ask_endpoint():
    response = client.get("/ask")
    assert response.status_code == 200
    assert "data" in response.json()

def test_post_ask_endpoint():
    response = client.post("/ask", json={"question": "Qual o pokemon que é um rato amarelo?"})
    assert response.status_code == 201
    assert response.json()["question"] == "Qual o pokemon que é um rato amarelo?"