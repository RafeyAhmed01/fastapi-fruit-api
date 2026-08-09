from pydantic import BaseModel, Field, field_validator

class CategoryCreate(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=12,
        description="The name of category",
        examples=["Citrus", "Berry"]
    )

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, value: str) -> str:
        trimmed_value = value.strip()
        if not trimmed_value:
            raise ValueError("Category name can't be empty or just spaces")
        return trimmed_value.title()

class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

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
    category_id: int

class FruitResponse(Fruit):
    id: int
    category: CategoryResponse

    class Config:
        from_attributes = True