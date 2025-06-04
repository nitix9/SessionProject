from fastapi import APIRouter, HTTPException, Depends
from auth import auth_handler
from database import get_db
from sqlalchemy.orm import Session
import models as m
from typing import List
import pyd

role_router=APIRouter(prefix="/role", tags=["role"])

@role_router.get("/", response_model=List[pyd.BaseRole])
def get_all_role(db:Session=Depends(get_db)):
    roles = db.query(m.Role).order_by(m.Role.id).all()
    return roles

@role_router.get("/{role_id}", response_model=pyd.BaseRole)
def get_role(role_id:int, db:Session=Depends(get_db)):
    role = db.query(m.Role).filter(m.Role.id==role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Роль не найдена")
    return role

@role_router.post("/", response_model=pyd.CreateRole)
def create_role(role:pyd.CreateRole, db:Session=Depends(get_db),current_user: m.User = Depends(auth_handler.auth_wrapper)):
    role_db=db.query(m.Role).filter(m.Role.name==role.name).first()
    if role_db:
        raise HTTPException(status_code=400, detail="Такая роль уже существует")
    role_db = m.Role()
    role_db.name = role.name
    db.add(role_db)
    db.commit()
    return role_db

@role_router.put("/{role_id}", response_model=pyd.CreateRole)
def update_role(role_id:int, role:pyd.CreateRole, db:Session=Depends(get_db),current_user: m.User = Depends(auth_handler.auth_wrapper)):
    role_db = db.query(m.Role).filter(m.Role.id==role_id).first()
    if not role_db:
        raise HTTPException(status_code=404, detail="Роль не найдена")
    role_db.name = role.name
    db.commit()
    return role_db

@role_router.delete("/{role_id}")
def delete_role(role_id:int, db:Session=Depends(get_db),current_user: m.User = Depends(auth_handler.auth_wrapper)):
    role = db.query(m.Role).filter(m.Role.id==role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Роль не найден")
    db.delete(role)
    db.commit()
    return {"msg":"Роль удалена"}