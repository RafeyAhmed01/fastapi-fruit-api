from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Fruit(BaseModel):

    name: str

fruits = []

@app.get("/")
def root():
    return {"routes available": ["/", "/fruits", "/fruits/{fruit_id}"]}

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

