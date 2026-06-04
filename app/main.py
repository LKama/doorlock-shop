from fastapi import FastAPI
from sqladmin import Admin
from app.database import engine

from app.admin import (
    UserAdmin,
    ProductAdmin,
    OrderAdmin
)

from app.database import Base, engine

from app.models.user import User
from app.models.product import Product
from app.models.cart_item import CartItem
from app.models.order import Order
from app.models.order_item import OrderItem

from app.routers.auth import router as auth_router
from app.routers.products import router as products_router
from app.routers.cart import router as cart_router
from app.routers.orders import router as orders_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DoorLock Shop API")

admin = Admin(app, engine)


admin.add_view(UserAdmin)
admin.add_view(ProductAdmin)
admin.add_view(OrderAdmin)

app.include_router(auth_router)
app.include_router(products_router)
app.include_router(cart_router)
app.include_router(orders_router)

@app.get("/")
def root():
  return {"message": "API WORKING"}