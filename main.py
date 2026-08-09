from fastapi import FastAPI, HTTPException, Depends, status, Query
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models
from database import engine, SessionLocal
import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fruit API with SQLite")

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()


@app.get("/")
def root():
    return {"routes available": 
            {"GET": ["/", "/fruits", "/fruits/{fruit_id}"],
             "POST": ["/fruits"], 
             "PUT": ["/fruits/{fruit_id}"], 
             "DELETE": ["/fruits/{fruit_id}"]
             }}


@app.get("/fruits", response_model=list[schemas.FruitResponse])
def get_all_fruits(# noqa: B008
    search: Optional[str] = Query(default=None, description="Search fruit by name"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(models.DBFRUIT)

    if search: 
        query = query.filter(models.DBFRUIT.name.ilike(f"%{search}%"))

    fruits =  query.offset(skip).limit(limit).all()
    return fruits


@app.post("/fruits", status_code=status.HTTP_201_CREATED, response_model=schemas.FruitResponse)
def add_fruit(fruit: schemas.FruitCreate, db: Session = Depends(get_db)):

    category = db.query(models.DBCategory).filter(models.DBCategory.id == fruit.category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detal=f"category with id = {fruit.category_id} not found")
    
    new_fruit = models.DBFRUIT(name=fruit.name, category_id=fruit.category_id)
    db.add(new_fruit)
    try:
        db.commit()
        db.refresh(new_fruit)
        return new_fruit
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"a fruit named {fruit.name} already exists")


@app.get("/fruits/{fruit_id}", response_model=schemas.FruitResponse)
def get_fruit(fruit_id: int, db: Session = Depends(get_db)): #noqa: B008
    db_fruit = db.query(models.DBFRUIT).filter(models.DBFRUIT.id == fruit_id).first()
    if db_fruit is None:
        raise HTTPException(status_code=404, detail="Fruit not found")
    return db_fruit


@app.put("/fruits/{fruit_id}", response_model=schemas.FruitResponse)
def update_fruit(fruit_id: int, updated_fruit: schemas.Fruit, db: Session = Depends(get_db)): #noqa: B008
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

@app.get("/category", response_model=list[schemas.CategoryResponse])
def get_all_categories(
    db: Session = Depends(get_db),
    skip: int = Query(ge=0, default=0),
    limit: int = Query(ge= 1, le=100, default=10)
    ):

    query = db.query(models.DBCategory)

    categories = query.offset(skip).limit(limit).all()
    return categories
    

@app.post("/category", status_code=status.HTTP_201_CREATED, response_model=schemas.CategoryResponse)
def create_category(new_category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = models.DBCategory(name=new_category.name)
    db.add(db_category)
    try: 
        db.commit()
        db.refresh(db_category)
        return db_category  
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Category named {new_category.name} already exists!")
        

