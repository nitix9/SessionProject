from fastapi import FastAPI
from routes.product import product_router
from routes.category import category_router
from routes.user import user_router
from routes.address import address_router
from routes.order_status import order_status_router
from routes.role import role_router
from routes.shop import shop_router

app = FastAPI()
app.include_router(product_router)
app.include_router(category_router)
app.include_router(user_router)
app.include_router(address_router)
app.include_router(order_status_router)
app.include_router(role_router)
app.include_router(shop_router)