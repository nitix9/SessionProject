from fastapi import HTTPException, Depends, Security,status,Request
from fastapi.security import  HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from config import settings
from datetime import datetime, timedelta, timezone
import jwt
import pyd
from jwt.exceptions import InvalidTokenError
from typing import Annotated, Optional
import models as m
from passlib.context import CryptContext

class AuthHandler:
    security_bearer = HTTPBearer()

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



    def verify_password(self,plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)


    def authenticate_user(self, username: str, password: str,db:Session=Depends(get_db)):
        user_db = db.query(m.User).filter(m.User.email==username).first()
        if not user_db:
            return False
        if not self.verify_password(password, user_db.password_hash):
            return False
        return user_db

    def get_user_by_email(self,db: Session, email: str) -> m.User | None:
        return db.query(m.User).filter(m.User.email == email).first()


    async def get_current_user(
        self,
        request: Request,
        credentials: Optional [HTTPAuthorizationCredentials] = Depends(security_bearer),
        db: Session = Depends(get_db)
    ):
        print("=== Debug get_current_user ===")
        print("Cookies:", request.cookies)
        print("Headers:", dict(request.headers))
        
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        token = None
            
        # Сначала проверяем куки
        token = request.cookies.get('access_token')
        print("Access token from cookies:", token)
        
        # Если нет в куках, используем токен из заголовка
        if not token:
            try:
                token = credentials.credentials
                print("Access token from header:", token)
            except:
                print("No token in header")
                raise credentials_exception
        
        try:
            # Декодируем токен
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            print("Decoded payload:", payload)
            username = payload["sub"]
            if username is None:
                print("No username in token")
                raise credentials_exception
            token_data = pyd.TokenData(email=username)
        except InvalidTokenError as e:
            print("Token decode error:", str(e))
            raise credentials_exception
        print (f'${token_data.email} - EMAIL!!!')    
        user = self.get_user_by_email(db, email=token_data.email)
        if user is None:
            print("User not found in database")
            raise credentials_exception
        print("User found:", user.email)
        return user


    def create_access_token(self,data: dict, expires_delta: timedelta | None = None):
        print("=== Debug create_access_token ===")
        print("Received expires_delta:", expires_delta)
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        print("Token will expire at:", expire)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    async def get_current_active_user(
        self,
        current_user: Annotated[m.User, Depends(get_current_user)],
    ):
        return current_user
    
    async def auth_wrapper(
    self,
    request: Request,
    credentials: Optional [HTTPAuthorizationCredentials] = Security(security_bearer),
    db: Session = Depends(get_db)):
         return await self.get_current_user(request, credentials, db)
    
auth_handler=AuthHandler()