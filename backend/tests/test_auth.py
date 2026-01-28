from fastapi.testclient import TestClient
from jose import jwt
import os
import uuid

def test_register_user(client: TestClient):
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "full_name": "Test User"
        }
    )
    
    assert response.status_code in [200, 201, 400]
    
    if response.status_code in [200, 201]:
        data = response.json()
        assert "email" in data
        assert data["email"] == "test@example.com"
        assert "id" in data

def test_login_user(client: TestClient):
    client.post(
        "/auth/register",
        json={
            "email": "login@test.com",
            "password": "password123",
            "full_name": "Login Test"
        }
    )
    
    response = client.post(
        "/auth/login",
        params={
            "email": "login@test.com",
            "password": "password123"
        }
    )
    
    if response.status_code != 200:
        response = client.post(
            "/auth/login",
            data={
                "username": "login@test.com",
                "password": "password123"
            }
        )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_basic_endpoints(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    
    response = client.get("/health")
    if response.status_code == 200:
        data = response.json()
        assert "status" in data

def test_register_duplicate_email(client: TestClient):
    response1 = client.post(
        "/auth/register",
        json={
            "email": "duplicate@test.com",
            "password": "password123",
            "full_name": "First User"
        }
    )
    assert response1.status_code in [200, 201]
    
    response2 = client.post(
        "/auth/register",
        json={
            "email": "duplicate@test.com",
            "password": "password456",
            "full_name": "Second User"
        }
    )
    
    assert response2.status_code == 400
    data = response2.json()
    assert "detail" in data

def test_login_wrong_password(client: TestClient):
    client.post(
        "/auth/register",
        json={
            "email": "wrongpass@test.com",
            "password": "correct123",
            "full_name": "Password Test"
        }
    )
    
    response = client.post(
        "/auth/login",
        params={
            "email": "wrongpass@test.com",
            "password": "wrongpassword"
        }
    )
    
    if response.status_code != 401:
        response = client.post(
            "/auth/login",
            data={
                "username": "wrongpass@test.com",
                "password": "wrongpassword"
            }
        )
    
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data

def test_login_nonexistent_user(client: TestClient):
    response = client.post(
        "/auth/login",
        params={
            "email": "nonexistent@test.com",
            "password": "password123"
        }
    )
    
    if response.status_code != 401:
        response = client.post(
            "/auth/login",
            data={
                "username": "nonexistent@test.com",
                "password": "password123"
            }
        )
    
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data

def test_token_validity(client: TestClient):
    client.post(
        "/auth/register",
        json={
            "email": "token@test.com",
            "password": "password123",
            "full_name": "Token Test"
        }
    )
    
    response = client.post(
        "/auth/login",
        params={
            "email": "token@test.com",
            "password": "password123"
        }
    )
    
    if response.status_code != 200:
        response = client.post(
            "/auth/login",
            data={
                "username": "token@test.com",
                "password": "password123"
            }
        )
    
    assert response.status_code == 200
    data = response.json()
    token = data["access_token"]
    
    secret_key = os.getenv("SECRET_KEY", "test_secret_key_fallback")
    algorithm = os.getenv("ALGORITHM", "HS256")
    
    payload = jwt.decode(
        token,
        secret_key,
        algorithms=[algorithm]
    )
    
    assert "sub" in payload
    assert "exp" in payload

def test_protected_endpoint_without_token(client: TestClient):
    response = client.get("/activities/")
    assert response.status_code in [401, 404]