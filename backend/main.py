from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175", "http://localhost:5176"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Pydantic Schemas ---

class UserCreate(BaseModel):
    username: str
    email: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


class TodoResponse(BaseModel):
    id: int
    title: str
    completed: bool
    owner_id: int | None = None

    class Config:
        from_attributes = True


class TodoCreate(BaseModel):
    title: str
    owner_id: int | None = None


class TodoUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None


# --- User Endpoints ---

@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = models.User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


# --- Todo Endpoints ---

@app.get("/todos", response_model=List[TodoResponse])
def get_todos(db: Session = Depends(get_db)):
    return db.query(models.Todo).all()


@app.post("/todos", response_model=TodoResponse, status_code=201)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    if todo.owner_id:
        user = db.query(models.User).filter(models.User.id == todo.owner_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
    db_todo = models.Todo(title=todo.title, completed=False, owner_id=todo.owner_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo.title is not None:
        db_todo.title = todo.title
    if todo.completed is not None:
        db_todo.completed = todo.completed
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()