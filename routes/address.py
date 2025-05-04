from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
import models as m
from typing import List
import pyd

address_router=APIRouter(prefix="/addresses", tags=["addresses"])

@address_router.get("/", response_model=List[pyd.BaseAddress])
def get_all_address(db:Session=Depends(get_db)):
    address= db.query(m.Address).all()
    return address

@address_router.get("/{id}",response_model=pyd.BaseAddress)
def get_address_byid(address_id:int,db:Session=Depends(get_db)):
    address=db.query(m.Address).filter(m.Address.id==address_id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Адрес не найден")
    return address


@address_router.post("/", response_model=pyd.BaseAddress)
def address_add(address: pyd.CreateAddress, db:Session=Depends(get_db)):
    address_db=m.Address()
    address_db.address=address.address
    address_db.user_id=address.user_id
    db.add(address_db)
    db.commit()
    return address_db

@address_router.put("/{address_id}", response_model=pyd.CreateAddress)
def update_address(address_id:int, address:pyd.CreateAddress, db:Session=Depends(get_db)):
    address_db = db.query(m.Address).filter(m.Address.id==address_id).first()
    if not address_db:
        raise HTTPException(status_code=404, detail="Адрес не найден")
    address_db.address=address.address
    address_db.user_id=address.user_id
    db.add(address_db)
    db.commit()
    return address_db

@address_router.delete("/{id}")
def delete_address (address_id:int, db:Session=Depends(get_db)):
    address=db.query(m.Address).filter(m.Address.id==address_id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Адрес не найден")
    db.delete(address)
    db.commit()
    return {"detail":"Адрес успешно удален"}