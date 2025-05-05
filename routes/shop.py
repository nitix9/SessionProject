from fastapi import APIRouter, HTTPException, Depends, UploadFile,Query
from database import get_db
from sqlalchemy.orm import Session
import models as m
from typing import List
import pyd
import uuid
from PIL import Image
import os
import io
from config import settings
from sqlalchemy import func

shop_router=APIRouter(prefix="/shop", tags=["shop"])

@shop_router.get("/", response_model=pyd.PaginatedShops)
def get_all_shops(db:Session=Depends(get_db),page: int = Query(1, ge=1),
    page_size: int = Query(10, le=100)
):
    total = db.query(func.count(m.Shop.id)).scalar()
    skip = (page - 1) * page_size
    shops = db.query(m.Shop).order_by(m.Shop.id).offset(skip).limit(page_size).all()
    return {
        "total": total,
        "items": shops,
        "page": page,
        "page_size": page_size
    }

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

@shop_router.put("/image/{product_id}", response_model=pyd.SchemaShop)
def upload_image(shop_id:int, image:UploadFile, db:Session=Depends(get_db)):
    shop_db=(
        db.query(m.Shop).filter(m.Shop.id==shop_id).first()
    )
    if not shop_db:
        raise HTTPException(status_code=404, detail="Магазин не найден")
    
    
    if image.content_type not in settings.ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Неверный тип файла")
    ext = image.filename.split(".")[-1].lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Недопустимое расширение файла")
    # Генерируем уникальное имя файла
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    contents = image.file.read()
    upload_dir = os.path.join("files", "shops")
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, unique_filename)
    if len(contents) > settings.MAX_FILE_SIZE:
        try:
            image_obj = Image.open(io.BytesIO(contents))

            # Преобразуем в RGB, если нужно
            if image_obj.mode in ("RGBA", "P"):
                image_obj = image_obj.convert("RGB")

            # Уменьшаем размер (по желанию)
            max_width, max_height = 1920, 1080
            image_obj.thumbnail((max_width, max_height))

            # Пробуем сохранить в памяти с уменьшением качества
            img_byte_arr = io.BytesIO()
            
            if ext in ["jpg", "jpeg"]:
                for quality in range(85, 10, -5):  # Попробуем от 85 до 15
                    img_byte_arr.seek(0)
                    img_byte_arr.truncate()
                    image_obj.save(img_byte_arr, format="JPEG", quality=quality, optimize=True)
                    if img_byte_arr.tell() <= settings.MAX_FILE_SIZE:
                        break

            elif ext == "png":
                # Для PNG просто оптимизируем — тут нет качества как у JPEG
                image_obj.save(img_byte_arr, format="PNG", optimize=True)

            else:
                raise HTTPException(status_code=400, detail="Неподдерживаемый формат")

            # Получаем содержимое
            img_byte_arr.seek(0)
            contents = img_byte_arr.read()

            if len(contents) > settings.MAX_FILE_SIZE:
                raise HTTPException(status_code=400, detail="Файл слишком большой, даже после сжатия")

            # Сохраняем на диск
            with open(file_path, "wb") as f:
                f.write(contents)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при обработке изображения: {e}")
    else:
        with open(file_path, "wb") as f:
                f.write(contents)
    shop_db.logo_path= file_path
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