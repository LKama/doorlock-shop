from sqladmin import ModelView

from app.models.user import User
from app.models.product import Product
from app.models.order import Order


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.name]


class ProductAdmin(ModelView, model=Product):
    column_list = [
        Product.id,
        Product.name,
        Product.price,
        Product.category,
        Product.stock,
    ]


class OrderAdmin(ModelView, model=Order):
    column_list = [
        Order.id,
        Order.user_id,
        Order.total_price,
        Order.status,
    ]