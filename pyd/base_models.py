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

class BaseUser(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example="Иван")
    last_name: str = Field(example="Иванов")
    patronymic: str = Field(example="Иванович")
    email: str = Field(example="example@mail.ru")
    phone: str = Field(example="+79123456789")

class BaseRole(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example="admin")

class BaseAddress(BaseModel):
    id: int = Field(example=1)
    address: str = Field(example="г. Москва, ул. Ленина, д. 1")

class BaseOrder(BaseModel):
    id: int = Field(example=1)
    total_price: float = Field(example=100.0)
    created_at: str = Field(example="2023-10-01T12:00:00")

class BaseOrderStatus(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example="Выполнен")

class BaseShop(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example="Магазин 1")
    description: str|None = Field(example="Магазин электроники")
    custom_domain:str = Field(example="example")
    logo_path: str|None = Field(example="path/to/logo.png")