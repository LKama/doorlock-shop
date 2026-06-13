from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import engine

from app.database import Base, engine

from app.models.user import User
from app.models.product import Product
from app.models.cart_item import CartItem
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.favorite import Favorite
from app.models.chat_message import ChatMessage


from app.routers.auth import router as auth_router
from app.routers.products import router as products_router
from app.routers.cart import router as cart_router
from app.routers.orders import router as orders_router
from app.routers.admin import router as admin_router
from app.routers.favorites import router as favorites_router
from app.routers.chat import router as chat_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DoorLock Shop API")

app.mount(
  "/static",
  StaticFiles(directory="static"),
  name="static"
)

app.include_router(auth_router)
app.include_router(products_router)
app.include_router(cart_router)
app.include_router(orders_router)
app.include_router(admin_router)

app.include_router(auth_router)
app.include_router(products_router)
app.include_router(cart_router)
app.include_router(orders_router)
app.include_router(favorites_router)
app.include_router(chat_router)

@app.get("/")
def root():
  return {"message": "API WORKING"}

