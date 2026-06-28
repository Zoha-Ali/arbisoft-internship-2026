from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class TodoResponse(BaseModel):
    id: int
    title: str
    completed: bool

    class Config:
        from_attributes = True


@app.get("/todos", response_model=List[TodoResponse])
def get_todos(db: Session = Depends(get_db)):
    return db.query(models.Todo).all()
