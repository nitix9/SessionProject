from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
import models as m
from typing import List
import pyd

product_router=APIRouter(prefix="/product", tags=["product"])

@product_router.get("/", response_model=List[pyd.SchemaProduct])
def get_all_product(db:Session=Depends(get_db)):
    products = db.query(m.Product).order_by(m.Product.id).all()
    return products

@product_router.get("/{product_id}", response_model=pyd.BaseProduct)
def get_product(product_id:int, db:Session=Depends(get_db)):
    product = db.query(m.Product).filter(m.Product.id==product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product

@product_router.post("/", response_model=pyd.CreateProduct)
def create_product(product:pyd.CreateProduct, db:Session=Depends(get_db)):
    product_db = m.Product()
    product_db.name = product.name
    product_db.description = product.description
    product_db.price = product.price
    product_db.image_path = product.image_path
    product_db.category_id = product.category_id
    db.add(product_db)
    db.commit()
    return product_db

@product_router.delete("/{product_id}")
def delete_product(product_id:int, db:Session=Depends(get_db)):
    product = db.query(m.Product).filter(m.Product.id==product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    db.delete(product)
    db.commit()
    return {"msg":"Товар удален"}