from pydantic import BaseModel, Field

class CreateProduct(BaseModel):
    name: str = Field(min_length=3,max_length=255,example="Молоко")
    price: float = Field(example=10.85)
    description: str= Field(example='Вкусное молоко')
    image_path: str= Field(example='dsdasd')
    category_id: int = Field(example=1)

class CreateCategory(BaseModel):
    name:str = Field(example="ЕДА")