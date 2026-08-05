from fastapi import FastAPI, HTTPException, Depends, status, Query
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fruit API with SQLite")


class Fruit(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=12,
        description="The name of fruit",
        examples=["Mango", "Banana"]
    )

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, value: str) -> str:
        trimmed_value = value.strip()
        if not trimmed_value:
            raise ValueError("Fruit name can't be empty or just spaces")
        return trimmed_value.title()

class FruitCreate(Fruit):
    pass

class FruitResponse(Fruit):
    id: int

    class Config:
        from_attributes = True

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()


@app.get("/")
def root():
    return {"routes available": {"GET": ["/", "/fruits", "/fruits/{fruit_id}"], "POST": ["/fruits"], "PUT": ["/fruits/{fruit_id}"], "DELETE": ["/fruits/{fruit_id}"]}}


@app.get("/fruits", response_model=list(FruitResponse))
def get_all_fruits(db: Session = Depends(get_db)): # noqa: B008
    skip: int = Query(default=-0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    fruits =  db.query(models.DBFRUIT).offset(skip).limit(limit).all()
    return


@app.post("/fruits", status_code=status.HTTP_201_CREATED, response_model=FruitResponse)
def add_fruit(fruit: FruitCreate, db: Session = Depends(get_db)):
    new_fruit = models.DBFRUIT(name=fruit.name)
    db.add(new_fruit)
    try:
        db.commit()
        db.refresh(new_fruit)
        return new_fruit
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"a fruit named {new_fruit} already exists")


@app.get("/fruits/{fruit_id}", response_model=FruitResponse)
def get_fruit(fruit_id: int, db: Session = Depends(get_db)): #noqa: B008
    db_fruit = db.query(models.DBFRUIT).filter(models.DBFRUIT.id == fruit_id).first()
    if db_fruit is None:
        raise HTTPException(status_code=404, detail="Fruit not found")
    return db_fruit


@app.put("/fruits/{fruit_id}", response_model=FruitResponse)
def update_fruit(fruit_id: int, updated_fruit: Fruit, db: Session = Depends(get_db)): #noqa: B008
    db_fruit = db.query(models.DBFRUIT).filter(models.DBFRUIT.id == fruit_id).first()
    if db_fruit is None:
        raise HTTPException(
            status_code=404, detail="Fruit doesn't exist"
        )
    db_fruit.name = updated_fruit.name
    db.commit()
    db.refresh(db_fruit)
    return {"fruit": db_fruit.name}

@app.delete("/fruits/{fruit_id}")
def delete_fruit(fruit_id: int, db: Session = Depends(get_db)): #noqa: B008
    db_fruit = db.query(models.DBFRUIT).filter(models.DBFRUIT.id == fruit_id).first()
    if db_fruit is None: 
        raise HTTPException(status_code=404, detail=f"Fruit with id={fruit_id} doesn't exist")
    db.delete(db_fruit)
    db.commit()
    return {"message": f"Successfully deleted {db_fruit.name}"}
