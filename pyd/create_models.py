from pydantic import BaseModel, Field
from typing import List
from .base_models import *

class CreateProduct(BaseModel):
    name: str = Field(min_length=3,max_length=255,example="Молоко")
    price: float = Field(example=10.85)
    description: str | None = Field(example='Вкусное молоко')
    category_id: int = Field(example=1)
    shop_id:int=Field(example=1)

class CreateCategory(BaseModel):
    name:str = Field(example="ЕДА")

class CreateUser(BaseModel):
    name: str = Field(example="Иван")
    last_name: str = Field(example="Иванов")
    password_hash:str=Field(example="qweqwqe123")
    patronymic: str | None = Field(example="Иванович")
    email: str = Field(example="example@mail.ru")
    role_id:int=Field(example=1)
    phone: str = Field(example="+79123456789")

class CreateRole(BaseModel):
    name: str = Field(example="admin")

class CreateAddress(BaseModel):
    address: str = Field(example="г. Москва, ул. Ленина, д. 1")
    user_id:int=Field(example=1)

class CreateOrder(BaseModel):
    user_id:int=Field(example=1)
    shop_id:int=Field(example=1)
    address_id:int=Field(example=1)
    products:List[BaseOrderProduct]

class CreateOrderStatus(BaseModel):
    name: str = Field(example="Выполнен")

class CreateShop(BaseModel):
    name: str = Field(example="Магазин 1")
    description: str | None = Field(example="Магазин электроники")
    custom_domain:str = Field(example="example")
    logo_path: str | None = Field(example="path/to/logo.png")
    user_id:int=Field(example=1)