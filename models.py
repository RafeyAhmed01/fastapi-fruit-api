from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class DBCategory(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    fruits = relationship("DBFRUIT", back_populates="category")

class DBFRUIT(Base):
    __tablename__ = "fruits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    category = relationship("DBCategory", back_populates="fruits")

