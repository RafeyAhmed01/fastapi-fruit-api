from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fruit API with SQLite")


class Fruit(BaseModel):
    name: str


fruits = []


@app.get("/")
def root():
    return {"routes available": {"GET": ["/", "/fruits", "/fruits/{fruit_id}"], "POST": ["/fruits"], "PUT": ["/fruits/{fruit_id}"], "DELETE": ["/fruits/{fruit_id}"]}}


@app.get("/fruits")
def get_all_fruits():
    return {"fruits": fruits}


@app.post("/fruits", status_code=201)
def add_fruit(fruit: Fruit):
    fruits.append(fruit)
    return fruit


@app.get("/fruits/{fruit_id}", response_model=Fruit)
def get_fruit(fruit_id: int):
    if fruit_id < 0 or fruit_id >= len(fruits):
        raise HTTPException(status_code=404, detail="Fruit ID out of range")
    return fruits[fruit_id]


@app.put("/fruits/{fruit_id}", response_model=Fruit)
def update_fruit(fruit_id: int, updated_fruit: Fruit):
    if fruit_id < 0 or fruit_id >= len(fruits):
        raise HTTPException(
            status_code=404, detail=f"Fruit with id={fruit_id} is out of range"
        )
    fruits[fruit_id] = updated_fruit
    return updated_fruit

@app.delete("/fruits/{fruit_id}")
def delete_fruit(fruit_id: int):
    if fruit_id < 0 or fruit_id >= len(fruits):
        raise HTTPException(status_code=404, detail=f"Fruit with id={fruit_id} doesn't exist")
    deleted_fruit = fruits.pop(fruit_id)
    return {"message": f"Successfully deleted {deleted_fruit.name}"}
