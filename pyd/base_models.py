from pydantic import BaseModel, Field

class BaseCategory(BaseModel):
    id:int = Field(example=1)
    name:str = Field(example="ЕДА")

class BaseProduct(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example="Молоко")
    price: float = Field(example=10.85)
    description: str= Field(example='Вкусное молоко')
    image_path: str= Field(example='dsdasd')