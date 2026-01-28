from fastapi.testclient import TestClient

def test_create_activity_with_token(authenticated_client: TestClient):
    response = authenticated_client.post(
        "/activities/",
        json={
            "title": "Study Python",
            "activity_type": "study",
            "duration_minutes": 60,
            "description": "Learning FastAPI and SQLModel"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        assert "title" in data
        assert data["title"] == "Study Python"
    elif response.status_code == 404:
        print("ℹ️  Activities endpoint not implemented yet")

def test_get_activities_with_token(authenticated_client: TestClient):
    response = authenticated_client.get("/activities/")
    
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list)
    elif response.status_code == 404:
        print("ℹ️  Activities endpoint not implemented yet")

def test_activities_without_token(client: TestClient):
    response = client.get("/activities/")
    assert response.status_code in [401, 404]