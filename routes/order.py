from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
import models as m
from typing import List
import pyd

order_router=APIRouter(prefix="/order", tags=["order"])

@order_router.get("/", response_model=List[pyd.SchemaOrder])
def get_all_order(db:Session=Depends(get_db)):
    orders = db.query(m.Order).order_by(m.Order.id).all()
    return orders

@order_router.get("/{order_id}", response_model=pyd.SchemaOrder)
def get_order(order_id:int, db:Session=Depends(get_db)):
    order = db.query(m.Order).filter(m.Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order

@order_router.post("/", response_model=pyd.SchemaOrder)
def create_order(order:pyd.CreateOrder, db:Session=Depends(get_db)):
    total_price = 0
    for item in order.products:
        product = db.query(m.Product).filter(m.Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Продукт {item.product_id} не найден")
        total_price += float(product.price) * item.quantity

    order_db = m.Order()
    order_db.user_id = order.user_id
    order_db.shop_id=order.shop_id
    order_db.total_price=total_price
    order_db.adress_id=order.address_id
    order_db.status_id=1
    db.add(order_db)
    db.commit()
    db.refresh(order_db) 

    for item in order.products:
        order_item = m.OrderItem(
            order_id=order_db.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(order_item)

    db.commit()
    return order_db

@order_router.put("/{order_id}", response_model=pyd.SchemaOrder)
def update_order(order_id:int, order:pyd.CreateOrder, db:Session=Depends(get_db)):
    order_db = db.query(m.Order).filter(m.Order.id==order_id).first()
    if not order_db:
        raise HTTPException(status_code=404, detail="Заказ не найден")
   
    total_price = 0
    for item in order.products:
        product = db.query(m.Product).filter(m.Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Продукт {item.product_id} не найден")
        total_price += float(product.price) * item.quantity

    order_db.user_id = order.user_id
    order_db.shop_id = order.shop_id
    order_db.adress_id = order.address_id
    order_db.status_id = 1
    order_db.total_price = total_price

    db.query(m.OrderItem).filter(m.OrderItem.order_id == order_id).delete()

    for item in order.products:
            order_item = m.OrderItem(
                order_id=order_db.id,
                product_id=item.product_id,
                quantity=item.quantity
            )
            db.add(order_item)

    db.commit()
    db.refresh(order_db)
    return order_db

@order_router.delete("/{order_id}")
def delete_order(order_id:int, db:Session=Depends(get_db)):
    order = db.query(m.Order).filter(m.Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    db.delete(order)
    db.commit()
    return {"msg":"Заказ удален"}