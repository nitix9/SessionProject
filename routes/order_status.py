from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
import models as m
from typing import List
import pyd

order_status_router=APIRouter(prefix="/order_status", tags=["order_status"])

@order_status_router.get("/", response_model=List[pyd.BaseOrderStatus])
def get_all_order_status(db:Session=Depends(get_db)):
    order_statuses = db.query(m.OrderStatus).order_by(m.OrderStatus.id).all()
    return order_statuses

@order_status_router.get("/{order_status_id}", response_model=pyd.BaseOrderStatus)
def get_order_status(order_status_id:int, db:Session=Depends(get_db)):
    order_status = db.query(m.OrderStatus).filter(m.OrderStatus.id==order_status_id).first()
    if not order_status:
        raise HTTPException(status_code=404, detail="Статус заказа не найден")
    return order_status

@order_status_router.post("/", response_model=pyd.CreateOrderStatus)
def create_order_status(order_status:pyd.CreateOrderStatus, db:Session=Depends(get_db)):
    order_status_db=db.query(m.OrderStatus).filter(m.OrderStatus.name==order_status.name).first()
    if order_status_db:
        raise HTTPException(status_code=400, detail="Такой статус заказа уже существует")
    order_status_db = m.OrderStatus()
    order_status_db.name = order_status.name
    db.add(order_status_db)
    db.commit()
    return order_status_db

@order_status_router.put("/{order_status_id}", response_model=pyd.CreateOrderStatus)
def update_order_status(order_status_id:int, order_status:pyd.CreateOrderStatus, db:Session=Depends(get_db)):
    order_status_db = db.query(m.OrderStatus).filter(m.OrderStatus.id==order_status_id).first()
    if not order_status_db:
        raise HTTPException(status_code=404, detail="Статус заказа не найден")
    order_status_db.name = order_status.name
    db.commit()
    return order_status_db

@order_status_router.delete("/{order_status_id}")
def delete_order_statusy(order_status_id:int, db:Session=Depends(get_db)):
    order_status = db.query(m.OrderStatus).filter(m.OrderStatus.id==order_status_id).first()
    if not order_status:
        raise HTTPException(status_code=404, detail="Статус заказа не найден")
    db.delete(order_status)
    db.commit()
    return {"msg":"Статус заказа удален"}