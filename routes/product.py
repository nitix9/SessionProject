from fastapi import APIRouter, HTTPException, Depends,UploadFile
from fastapi import APIRouter, HTTPException, Depends,UploadFile
from database import get_db
from sqlalchemy.orm import Session
import models as m
from typing import List
import pyd
from config import settings
import uuid
from PIL import Image
import os
import io
from config import settings
import uuid
from PIL import Image
import os
import io

product_router=APIRouter(prefix="/product", tags=["product"])

@product_router.get("/", response_model=List[pyd.SchemaProduct])
def get_all_product(db:Session=Depends(get_db)):
    products = db.query(m.Product).order_by(m.Product.id).all()
    return products

@product_router.get("/{product_id}", response_model=pyd.BaseProduct)
def get_product(product_id:int, db:Session=Depends(get_db)):
    product = db.query(m.Product).filter(m.Product.id==product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product

@product_router.post("/", response_model=pyd.CreateProduct)
def create_product(product:pyd.CreateProduct, db:Session=Depends(get_db)):
    product_db = m.Product()
    product_db.name = product.name
    product_db.description = product.description
    product_db.price = product.price
    product_db.image_path = product.image_path
    product_db.category_id = product.category_id
    product_db.shop_id=product.shop_id
    db.add(product_db)
    db.commit()
    return product_db

@product_router.put("/image/{product_id}", response_model=pyd.SchemaProduct)
def upload_image(product_id:int, image:UploadFile, db:Session=Depends(get_db)):
    product_db=(
        db.query(m.Product).filter(m.Product.id==product_id).first()
    )
    if not product_db:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    
    
    if image.content_type not in settings.ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Неверный тип файла")
    ext = image.filename.split(".")[-1].lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Недопустимое расширение файла")
    # Генерируем уникальное имя файла
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    contents = image.file.read()
    upload_dir = os.path.join("files", "products")
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
    product_db.image_path= file_path
    db.commit()
    return product_db

@product_router.put("/{product_id}", response_model=pyd.CreateProduct)
def update_product(product_id:int, product:pyd.CreateProduct, db:Session=Depends(get_db)):
    product_db = db.query(m.Product).filter(m.Product.id==product_id).first()
    if not product_db:
        raise HTTPException(status_code=404, detail="Товар не найден")
    product_db.name = product.name
    product_db.description = product.description
    product_db.price = product.price
    product_db.category_id = product.category_id
    db.commit()
    return product_db

@product_router.delete("/{product_id}")
def delete_product(product_id:int, db:Session=Depends(get_db)):
    product = db.query(m.Product).filter(m.Product.id==product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    db.delete(product)
    db.commit()
    return {"msg":"Товар удален"}