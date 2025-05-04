from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
import models as m
from typing import List
import pyd

shop_router=APIRouter(prefix="/shop", tags=["shop"])

@shop_router.get("/", response_model=List[pyd.SchemaShop])
def get_all_shops(db:Session=Depends(get_db)):
    shops = db.query(m.Shop).order_by(m.Shop.id).all()
    return shops

@shop_router.get("/{shop_id}", response_model=pyd.SchemaShop)
def get_shop(shop_id:int, db:Session=Depends(get_db)):
    shop = db.query(m.Shop).filter(m.Shop.id==shop_id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Магазин не найден")
    return shop

@shop_router.post("/", response_model=pyd.CreateShop)
def create_shop(shop:pyd.CreateShop, db:Session=Depends(get_db)):
    shop_db=db.query(m.Shop).filter(m.Shop.custom_domain==shop.custom_domain).first()
    if shop_db:
        raise HTTPException(status_code=400, detail="Магазин с таким доменом уже существует")
    shop_db = m.Shop()
    shop_db.user_id=shop.user_id
    shop_db.name = shop.name
    shop_db.description=shop.description
    shop_db.custom_domain=shop.custom_domain
    shop_db.logo_path=shop.logo_path
    db.add(shop_db)
    db.commit()
    return shop_db

@shop_router.put("/{shop_id}", response_model=pyd.CreateShop)
def update_shop(shop_id:int, shop:pyd.CreateShop, db:Session=Depends(get_db)):
    shop_db = db.query(m.Shop).filter(m.Shop.id==shop_id).first()
    if not shop_db:
        raise HTTPException(status_code=404, detail="Магазин не найден")
    shop_db.user_id=shop.user_id
    shop_db.name = shop.name
    shop_db.description=shop.description
    shop_db.custom_domain=shop.custom_domain
    shop_db.logo_path=shop.logo_path
    db.commit()
    return shop_db

@shop_router.delete("/{shop_id}")
def delete_shop(shop_id:int, db:Session=Depends(get_db)):
    shop = db.query(m.Shop).filter(m.Shop.id==shop_id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Магазин не найден")
    db.delete(shop)
    db.commit()
    return {"msg":"Магазин удален"}