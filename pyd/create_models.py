from pydantic import BaseModel, Field

class CreateProduct(BaseModel):
    name: str = Field(min_length=3,max_length=255,example="Молоко")
    price: float = Field(example=10.85)
    description: str | None = Field(example='Вкусное молоко')
    image_path: str | None = Field(example='dsdasd')
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
    total_price: float = Field(example=100.0)
    created_at: str = Field(example="2023-10-01T12:00:00")

class CreateOrderStatus(BaseModel):
    name: str = Field(example="Выполнен")

class CreateShop(BaseModel):
    name: str = Field(example="Магазин 1")
    description: str | None = Field(example="Магазин электроники")
    custom_domain:str = Field(example="example")
    logo_path: str | None = Field(example="path/to/logo.png")