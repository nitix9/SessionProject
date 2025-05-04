from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
import models as m
from typing import List
import pyd

user_router=APIRouter(prefix="/users", tags=["users"])

@user_router.get("/", response_model=List[pyd.SchemaUser])
def get_all_users(db:Session=Depends(get_db)):
    users= db.query(m.User).all()
    return users

@user_router.get("/{id}",response_model=pyd.BaseUser)
def get_user_byid(user_id:int,db:Session=Depends(get_db)):
    user=db.query(m.User).filter(m.User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


@user_router.post("/", response_model=pyd.BaseUser)
def user_reg(user: pyd.CreateUser, db:Session=Depends(get_db)):
    user_db=db.query(m.User).filter(m.User.email==user.email).first()
    if user_db:
        raise HTTPException(status_code=400, detail="User already exists")
    user_db=m.User()
    user_db.name=user.name
    user_db.last_name=user.last_name
    user_db.patronymic=user.patronymic
    user_db.email=user.email
    user_db.role_id=user.role_id
    user_db.password_hash=user.password_hash
    user_db.phone=user.phone
    db.add(user_db)
    db.commit()
    return user_db

@user_router.put("/{user_id}", response_model=pyd.CreateUser)
def update_user(user_id:int, user:pyd.CreateUser, db:Session=Depends(get_db)):
    user_db = db.query(m.User).filter(m.User.id==user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    user_db.name=user.name
    user_db.last_name=user.last_name
    user_db.patronymic=user.patronymic
    user_db.email=user.email
    user_db.role_id=user.role_id
    user_db.password_hash=user.password_hash
    user_db.phone=user.phone
    db.add(user_db)
    db.commit()
    return user_db

@user_router.delete("/{id}")
def delete_user (user_id:int, db:Session=Depends(get_db)):
    user=db.query(m.User).filter(m.User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    db.delete(user)
    db.commit()
    return {"detail":"Пользователь успешно удален"}