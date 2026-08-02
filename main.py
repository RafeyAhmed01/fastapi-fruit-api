from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fruit API with SQLite")


class Fruit(BaseModel):
    name: str


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


@app.get("/fruits")
def get_all_fruits(db: Session = Depends(get_db)): # noqa: B008
    return db.query(models.DBFRUIT).all()


@app.post("/fruits", status_code=201, response_model=FruitResponse)
def add_fruit(fruit: Fruit, db: Session = Depends(get_db)):
    new_fruit = models.DBFRUIT(name=fruit.name)
    db.add(new_fruit)
    db.commit()
    db.refresh(new_fruit)
    return new_fruit


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
    return db_fruit

@app.delete("/fruits/{fruit_id}")
def delete_fruit(fruit_id: int, db: Session = Depends(get_db)): #noqa: B008
    db_fruit = db.query(models.DBFRUIT).filter(models.DBFRUIT.id == fruit_id).first()
    if db_fruit is None: 
        raise HTTPException(status_code=404, detail=f"Fruit with id={fruit_id} doesn't exist")
    db.delete(db_fruit)
    db.commit()
    return {"message": f"Successfully deleted {db_fruit.name}"}
