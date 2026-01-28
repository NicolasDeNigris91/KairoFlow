import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, SQLModel, Session
from sqlmodel.pool import StaticPool
import sys
import os
import warnings
import uuid
import logging

warnings.filterwarnings("ignore", message="Accessing argon2.__version__")
warnings.filterwarnings("ignore", category=DeprecationWarning)

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from main import app
from app.core.database import get_session


def pytest_configure():
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False
    )
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def authenticated_client(client: TestClient):
    test_email = f"auth_{uuid.uuid4().hex[:8]}@test.com"
    
    client.post(
        "/auth/register",
        json={
            "email": test_email,
            "password": "password123",
            "full_name": "Auth User"
        }
    )
    
    response = client.post(
        "/auth/login",
        params={
            "email": test_email,
            "password": "password123"
        }
    )
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        client.headers.update({"Authorization": f"Bearer {token}"})
    
    return client


@pytest.fixture
def unauthenticated_client(client: TestClient):
    if "Authorization" in client.headers:
        del client.headers["Authorization"]
    return client