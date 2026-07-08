import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models
from database import get_db
from main import app

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def reset_db():
    models.Base.metadata.create_all(bind=engine)
    yield
    models.Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    return TestClient(app)


def test_get_todos_empty(client):
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []


def test_create_todo(client):
    response = client.post("/todos", json={"title": "Buy milk"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy milk"
    assert data["completed"] is False
    assert "id" in data


def test_create_todo_appears_in_list(client):
    client.post("/todos", json={"title": "Buy milk"})
    response = client.get("/todos")
    assert len(response.json()) == 1


def test_update_todo_title(client):
    created = client.post("/todos", json={"title": "Old title"}).json()
    response = client.put(f"/todos/{created['id']}", json={"title": "New title"})
    assert response.status_code == 200
    assert response.json()["title"] == "New title"


def test_update_todo_completed(client):
    created = client.post("/todos", json={"title": "Task"}).json()
    response = client.put(f"/todos/{created['id']}", json={"completed": True})
    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_update_todo_not_found(client):
    response = client.put("/todos/999", json={"title": "Ghost"})
    assert response.status_code == 404


def test_delete_todo(client):
    created = client.post("/todos", json={"title": "Delete me"}).json()
    response = client.delete(f"/todos/{created['id']}")
    assert response.status_code == 204


def test_delete_todo_removes_from_list(client):
    created = client.post("/todos", json={"title": "Delete me"}).json()
    client.delete(f"/todos/{created['id']}")
    todos = client.get("/todos").json()
    assert all(t["id"] != created["id"] for t in todos)


def test_delete_todo_not_found(client):
    response = client.delete("/todos/999")
    assert response.status_code == 404


def test_create_user(client):
    response = client.post("/users", json={"username": "zoha", "email": "zoha@example.com"})
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "zoha"
    assert data["email"] == "zoha@example.com"
    assert "id" in data


def test_create_user_duplicate_email(client):
    client.post("/users", json={"username": "zoha", "email": "zoha@example.com"})
    response = client.post("/users", json={"username": "other", "email": "zoha@example.com"})
    assert response.status_code == 400


def test_get_users_empty(client):
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == []


def test_get_users_returns_created_user(client):
    client.post("/users", json={"username": "zoha", "email": "zoha@example.com"})
    response = client.get("/users")
    assert len(response.json()) == 1
    assert response.json()[0]["username"] == "zoha"


def test_create_todo_invalid_owner_id(client):
    response = client.post("/todos", json={"title": "Orphan todo", "owner_id": 999})
    assert response.status_code == 404