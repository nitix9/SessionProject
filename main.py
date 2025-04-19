from fastapi import FastAPI
from routes.product import product_router
from routes.category import category_router

app = FastAPI()
app.include_router(product_router)
app.include_router(category_router)