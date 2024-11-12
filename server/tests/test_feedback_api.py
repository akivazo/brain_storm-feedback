import pytest

from flask.testing import FlaskClient
from mongomock import MongoClient
from ..feedback_api import server, set_mongo_client

@pytest.fixture
def client():
    # Create a mock MongoDB client
    mock_mongo_client = MongoClient()
    set_mongo_client(mock_mongo_client)
    server.config['TESTING'] = True
    # Set up Flask test client
    client = server.test_client()
    yield client
    mock_mongo_client.close()


def test_add_feedback(client: FlaskClient):
    response = client.post("/feedback", json={"idea_id": "123", "owner_name": "akiva1", "content": "feedback"})

    assert response.status_code == 201
    assert "id" in response.get_json()

def test_add_feedback_missing_data(client: FlaskClient):
    response = client.post("/feedback", json={"owner_name": "akiva1", "content": "feedback"})

    assert response.status_code == 400
    assert "error" in response.get_json()

def test_get_feedbacks(client: FlaskClient):
    id1 = client.post("/feedback", json={"idea_id": "123", "owner_name": "akiva1", "content": "feedback"}).get_json()["id"]
    id2 = client.post("/feedback", json={"idea_id": "123", "owner_name": "akiva2", "content": "feedback"}).get_json()["id"]
    id3 = client.post("/feedback", json={"idea_id": "345", "owner_name": "akiva3", "content": "feedback"}).get_json()["id"]

    response = client.get("/feedbacks/123")

    assert response.status_code == 302
    feedbacks = response.get_json()["feedbacks"]

    assert feedbacks == [{"owner_name": "akiva1", "content": "feedback", "id": id1}, {"owner_name": "akiva2", "content": "feedback", "id": id2}]

    response = client.get("/feedbacks/345")

    assert response.status_code == 302
    feedbacks = response.get_json()["feedbacks"]

    assert feedbacks == [{"owner_name": "akiva3", "content": "feedback", "id": id3}]

def test_delete_feedback(client: FlaskClient):
    id1 = client.post("/feedback", json={"idea_id": "123", "owner_name": "akiva1", "content": "feedback"}).get_json()["id"]
    id2 = client.post("/feedback", json={"idea_id": "123", "owner_name": "akiva2", "content": "feedback"}).get_json()["id"]
    client.post("/feedback", json={"idea_id": "345", "owner_name": "akiva3", "content": "feedback"}).get_json()["id"]
    
    response = client.get("/feedbacks/123")

    feedbacks = response.get_json()["feedbacks"]

    assert feedbacks == [{"owner_name": "akiva1", "content": "feedback", "id": id1}, {"owner_name": "akiva2", "content": "feedback", "id": id2}]

    response = client.delete(f"/feedback/123/{id1}")

    assert response.status_code == 204

    response = client.get("/feedbacks/123")

    assert response.status_code == 302

    feedbacks = response.get_json()["feedbacks"]

    assert feedbacks == [{"owner_name": "akiva2", "content": "feedback", "id": id2}]

def test_delete_feedbacks(client: FlaskClient):
    client.post("/feedback", json={"idea_id": "123", "owner_name": "akiva1", "content": "feedback"})
    client.post("/feedback", json={"idea_id": "123", "owner_name": "akiva2", "content": "feedback"})
    client.post("/feedback", json={"idea_id": "345", "owner_name": "akiva3", "content": "feedback"})
    client.post("/feedback", json={"idea_id": "345", "owner_name": "akiva4", "content": "feedback"})

    response = client.get("/feedbacks/123")

    assert response.status_code == 302
    feedbacks = response.get_json()["feedbacks"]

    assert len(feedbacks) == 2

    response = client.delete("/feedbacks/123")

    assert response.status_code == 204

    response = client.get("/feedbacks/123")

    assert response.status_code == 200

    assert [] == response.get_json()["feedbacks"]

    response = client.get("/feedbacks/345")

    assert response.status_code == 302
    feedbacks = response.get_json()["feedbacks"]

    assert len(feedbacks) == 2

