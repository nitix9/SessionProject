from fastapi import HTTPException, Depends,APIRouter,status,Response,Cookie,Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db
import models
from auth import auth_handler
from config import settings
from datetime import datetime, timedelta, timezone
import jwt
import pyd
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
import models as m
from passlib.context import CryptContext


auth_router=APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/users/me/", response_model=pyd.BaseUser)
async def read_users_me(
    current_user: Annotated[pyd.BaseUser, Depends(auth_handler.auth_wrapper)],
):
    return current_user

@auth_router.post("/refresh")
async def refresh_access_token(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    # Сначала проверяем куки
    refresh_token = request.cookies.get('refresh_token')
    if not refresh_token:
        # Если нет в куках, проверяем заголовок Authorization
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        refresh_token = auth_header.split(' ')[1]
    
    try:
        # Декодируем refresh token
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload["sub"]
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Проверяем существование пользователя
    user = auth_handler.get_user_by_email(db, email=email)
    if not user or user.refresh_token != refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User refresh token not found"
        )
    
    # Создаем новый access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_handler.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    # Создаем новый refresh token
    new_refresh_token = auth_handler.create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    user.refresh_token=new_refresh_token
    db.commit()
    # Устанавливаем токены в куки
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite='lax',
        path='/',
        domain=None,
        max_age=60 * settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=False,
        samesite='lax',
        path='/',
        domain=None,
        max_age=60 * 60 * 24 * settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    
    # Возвращаем токены в ответе
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

@auth_router.post("/")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
    db: Session = Depends(get_db)
):
    
    user = auth_handler.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        print("Authentication failed")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    
    # Создаем access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    print("Creating access token with expiration:", access_token_expires)
    access_token = auth_handler.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    
    # Создаем refresh token
    refresh_token = auth_handler.create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    user.refresh_token=refresh_token
    db.commit()
    # Устанавливаем токены в куки
    cookie_options = {
        "key": "access_token",
        "value": access_token,
        "httponly": True,
        "secure": False,
        "samesite": "lax",
        "path": "/",
        "domain": None,
        "max_age": 60 * settings.ACCESS_TOKEN_EXPIRE_MINUTES
    }

    response.set_cookie(**cookie_options)
    
    cookie_options = {
        "key": "refresh_token",
        "value": refresh_token,
        "httponly": True,
        "secure": False,
        "samesite": "lax",
        "path": "/",
        "domain": None,
        "max_age": 60 * 60 * 24 * settings.REFRESH_TOKEN_EXPIRE_DAYS
    }

    response.set_cookie(**cookie_options)
    

    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@auth_router.post("/logout")
async def logout(
    response: Response,
    current_user: Annotated[m.User, Depends(auth_handler.auth_wrapper)],
    db: Session = Depends(get_db)
):
    # Удаляем куки
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    current_user.refresh_token=None
    db.commit()
    
    return {"message": "Successfully logged out"}

@auth_router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[pyd.BaseUser, Depends(auth_handler.auth_wrapper)],
):
    return [{"item_id": "Foo", "owner": current_user.email}]