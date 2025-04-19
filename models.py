from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DECIMAL
from sqlalchemy.orm import relationship

class Category(Base):#1
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True,nullable=False)

class Product(Base):#N
    __tablename__ = "products"

    # backref автоматически делает связь в другой таблице
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255),nullable=False)
    price = Column(DECIMAL,nullable=False)
    description = Column(String(255))
    image_path= Column(String(255),nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"),nullable=False)

    category=relationship("Category", backref="products")
