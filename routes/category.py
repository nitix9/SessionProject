from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
import models as m
from typing import List
import pyd

category_router=APIRouter(prefix="/category", tags=["category"])

@category_router.get("/", response_model=List[pyd.BaseCategory])
def get_all_category(db:Session=Depends(get_db)):
    categories = db.query(m.Category).order_by(m.Category.id).all()
    return categories

@category_router.get("/{category_id}", response_model=pyd.BaseCategory)
def get_category(category_id:int, db:Session=Depends(get_db)):
    category = db.query(m.Category).filter(m.Category.id==category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return category

@category_router.post("/", response_model=pyd.CreateCategory)
def create_category(category:pyd.CreateCategory, db:Session=Depends(get_db)):
    category_db=db.query(m.Category).filter(m.Category.name==category.name).first()
    if category_db:
        raise HTTPException(status_code=400, detail="Такая категория уже существует")
    category_db = m.Category()
    category_db.name = category.name
    db.add(category_db)
    db.commit()
    return category_db

@category_router.put("/{category_id}", response_model=pyd.CreateCategory)
def update_category(category_id:int, category:pyd.CreateCategory, db:Session=Depends(get_db)):
    category_db = db.query(m.Category).filter(m.Category.id==category_id).first()
    if not category_db:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    category_db.name = category.name
    db.commit()
    return category_db

@category_router.delete("/{category_id}")
def delete_category(category_id:int, db:Session=Depends(get_db)):
    category = db.query(m.Category).filter(m.Category.id==category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найден")
    db.delete(category)
    db.commit()
    return {"msg":"Категория удалена"}