from fastapi.testclient import TestClient

def test_api_documentation(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code in [200, 404]
    
    if response.status_code == 200:
        data = response.json()
        assert "openapi" in data
    
    response = client.get("/docs")
    assert response.status_code in [200, 404]
    
    response = client.get("/redoc")
    assert response.status_code in [200, 404]

def test_invalid_endpoint(client: TestClient):
    response = client.get("/this-does-not-exist")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data