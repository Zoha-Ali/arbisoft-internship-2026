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


@pytest.fixture()
def auth_token(client):
    res = client.post(
        "/auth/signup",
        json={"username": "testuser", "email": "test@example.com", "password": "password123"},
    )
    assert res.status_code == 201
    return res.json()["access_token"]


@pytest.fixture()
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


# --- GET /todos ---

def test_get_todos_empty(client, auth_headers):
    response = client.get("/todos", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


def test_get_todos_without_token_returns_401(client):
    response = client.get("/todos")
    assert response.status_code == 401


# --- POST /todos ---

def test_create_todo(client, auth_headers):
    response = client.post("/todos", json={"title": "Buy milk"}, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy milk"
    assert data["completed"] is False
    assert "id" in data


def test_create_todo_appears_in_list(client, auth_headers):
    client.post("/todos", json={"title": "Buy milk"}, headers=auth_headers)
    response = client.get("/todos", headers=auth_headers)
    assert len(response.json()) == 1


# --- PUT /todos/{id} ---

def test_update_todo_title(client, auth_headers):
    created = client.post("/todos", json={"title": "Old title"}, headers=auth_headers).json()
    response = client.put(f"/todos/{created['id']}", json={"title": "New title"}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "New title"


def test_update_todo_completed(client, auth_headers):
    created = client.post("/todos", json={"title": "Task"}, headers=auth_headers).json()
    response = client.put(f"/todos/{created['id']}", json={"completed": True}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_update_todo_not_found(client, auth_headers):
    response = client.put("/todos/999", json={"title": "Ghost"}, headers=auth_headers)
    assert response.status_code == 404


# --- DELETE /todos/{id} ---

def test_delete_todo(client, auth_headers):
    created = client.post("/todos", json={"title": "Delete me"}, headers=auth_headers).json()
    response = client.delete(f"/todos/{created['id']}", headers=auth_headers)
    assert response.status_code == 204


def test_delete_todo_removes_from_list(client, auth_headers):
    created = client.post("/todos", json={"title": "Delete me"}, headers=auth_headers).json()
    client.delete(f"/todos/{created['id']}", headers=auth_headers)
    todos = client.get("/todos", headers=auth_headers).json()
    assert all(t["id"] != created["id"] for t in todos)


def test_delete_todo_not_found(client, auth_headers):
    response = client.delete("/todos/999", headers=auth_headers)
    assert response.status_code == 404


# --- POST /todos with invalid owner_id ---

def test_create_todo_invalid_owner_id(client, auth_headers):
    response = client.post("/todos", json={"title": "Orphan todo", "owner_id": 999}, headers=auth_headers)
    assert response.status_code == 404


# --- POST /auth/signup ---

def test_signup_success(client):
    response = client.post(
        "/auth/signup",
        json={"username": "zoha", "email": "zoha@example.com", "password": "secret123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "zoha"
    assert data["email"] == "zoha@example.com"
    assert "id" in data
    assert "access_token" in data
    assert "refresh_token" in data


def test_signup_duplicate_email(client):
    payload = {"username": "zoha", "email": "zoha@example.com", "password": "secret123"}
    client.post("/auth/signup", json=payload)
    response = client.post("/auth/signup", json={**payload, "username": "other"})
    assert response.status_code == 400


def test_signup_duplicate_username(client):
    client.post("/auth/signup", json={"username": "zoha", "email": "a@example.com", "password": "secret123"})
    response = client.post("/auth/signup", json={"username": "zoha", "email": "b@example.com", "password": "secret123"})
    assert response.status_code == 400


# --- POST /auth/login ---

def test_login_success(client):
    client.post("/auth/signup", json={"username": "zoha", "email": "zoha@example.com", "password": "secret123"})
    response = client.post("/auth/login", json={"email": "zoha@example.com", "password": "secret123"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post("/auth/signup", json={"username": "zoha", "email": "zoha@example.com", "password": "secret123"})
    response = client.post("/auth/login", json={"email": "zoha@example.com", "password": "wrongpassword"})
    assert response.status_code == 401


def test_login_unknown_email(client):
    response = client.post("/auth/login", json={"email": "nobody@example.com", "password": "secret123"})
    assert response.status_code == 401


# --- GET /users ---

def test_get_users_empty(client):
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == []


def test_get_users_returns_created_user(client):
    client.post("/auth/signup", json={"username": "zoha", "email": "zoha@example.com", "password": "secret123"})
    response = client.get("/users")
    assert len(response.json()) == 1
    assert response.json()[0]["username"] == "zoha"
