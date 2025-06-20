from database import Base
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Table, DECIMAL, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import backref

class Category(Base):#1
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True,nullable=False)

class Product(Base):#N
    __tablename__ = "products"

    # backref автоматически делает связь в другой таблице
    id = Column(Integer, primary_key=True, autoincrement=True)
    shop_id = Column(Integer, ForeignKey("shops.id",ondelete="CASCADE"),nullable=False)
    name = Column(String(255),nullable=False)
    price = Column(DECIMAL,nullable=False)
    description = Column(Text)
    image_path= Column(String(255),nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"),nullable=False)

    category=relationship("Category", backref="products")

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True,nullable=False)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255),nullable=False)
    last_name = Column(String(255),nullable=False)
    patronymic = Column(String(255),nullable=True)
    email = Column(String(255),unique=True,nullable=False)
    password_hash= Column(String(255),nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"),nullable=False)
    created_at = Column(DateTime(), server_default=func.now())
    phone= Column(String(255),nullable=True)
    refresh_token=Column(String(1024),nullable=True)

    role=relationship("Role", backref="users")
    addresses = relationship("Address", backref="user", cascade="all, delete-orphan")
    shops = relationship("Shop", backref="user", cascade="all, delete-orphan")
    orders = relationship("Order", backref="user", cascade="all, delete-orphan")


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
    address = Column(String(255),nullable=False)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    shop_id= Column(Integer, ForeignKey("shops.id",ondelete="CASCADE"),nullable=False)
    status_id = Column(Integer, ForeignKey("order_statuses.id"),nullable=False)
    total_price = Column(DECIMAL,nullable=False)
    adress_id = Column(Integer, ForeignKey("addresses.id",ondelete="CASCADE"),nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    shop=relationship("Shop", backref="orders")
    address=relationship("Address", backref="orders")
    status=relationship("OrderStatus", backref="orders")
    

class OrderStatus(Base):
    __tablename__ = "order_statuses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True,nullable=False)

class Shop(Base):
    __tablename__ = "shops"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    name = Column(String(255), unique=True,nullable=False)
    description = Column(String(255),nullable=True)
    custom_domain = Column(String(255),nullable=True)
    logo_path = Column(String(255),nullable=True)
    is_approved=Column(Boolean, nullable=False, default=False)

    products = relationship("Product", backref="shop", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", backref=backref("items", cascade="all, delete-orphan"))
    product = relationship("Product")