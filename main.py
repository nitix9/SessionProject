from fastapi import FastAPI
from routes.product import product_router
from routes.category import category_router
from routes.user import user_router
from routes.address import address_router
from routes.order_status import order_status_router
from routes.role import role_router
from routes.shop import shop_router
from routes.order import order_router
from routes.authr import auth_router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://26.0.93.75:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(product_router)
app.include_router(category_router)
app.include_router(user_router)
app.include_router(address_router)
app.include_router(order_status_router)
app.include_router(role_router)
app.include_router(shop_router)
app.include_router(order_router)
app.include_router(auth_router)

app.mount("/files", StaticFiles(directory="files"), name="files")