import threading

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.cart_item import CartItem
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product

from app.utils.dependencies import get_current_user
from app.utils.email import send_order_email

router = APIRouter(
  prefix="/orders",
  tags=["Orders"]
)

@router.post("/create")
def create_order(
  address: str,
  phone: str,
  current_user = Depends(get_current_user),
  db: Session = Depends(get_db)
):

  cart_items = db.query(CartItem).filter(
    CartItem.user_id == current_user.id
  ).all()

  if not cart_items:
    raise HTTPException(
      status_code=400,
      detail="Cart is empty"
    )

  total = 0

  for item in cart_items:
    total += item.product.price * item.quantity

  order = Order(
    user_id=current_user.id,
    total_price=total,
    address=address,
    phone=phone,
    status="pending"
  )

  db.add(order)
  db.commit()
  db.refresh(order)

  for item in cart_items:

    order_item = OrderItem(
      order_id=order.id,
      product_id=item.product_id,
      quantity=item.quantity,
      price_at_moment=item.product.price
    )

    db.add(order_item)

    db.delete(item)

  db.commit()

  products = []

  for item in cart_items:

    products.append({
      "name": item.product.name,
      "price": item.product.price,
      "quantity": item.quantity,
      "image_url": item.product.image_url
    })

  threading.Thread(
    target=send_order_email,
    args=(
      current_user.email,
      order.id,
      address,
      phone,
      products,
      total
    )
  ).start()

  return {
    "message": "Order created",
    "order_id": order.id
  }

@router.get("/")
def get_orders(
  current_user = Depends(get_current_user),
  db: Session = Depends(get_db)
):

  return db.query(Order).filter(
    Order.user_id == current_user.id
  ).all()

@router.get("/{order_id}")
def get_order_details(
  order_id: int,
  current_user=Depends(get_current_user),
  db: Session = Depends(get_db)
):

  order = db.query(Order).filter(
    Order.id == order_id,
    Order.user_id == current_user.id
  ).first()

  if not order:
    raise HTTPException(
      status_code=404,
      detail="Order not found"
    )

  items = []

  order_items = db.query(OrderItem).filter(
    OrderItem.order_id == order.id
  ).all()

  for item in order_items:

    product = db.query(Product).filter(
      Product.id == item.product_id
    ).first()

    items.append({
      "id": item.id,
      "quantity": item.quantity,
      "price": item.price_at_moment,
      "product": {
        "id": product.id,
        "name": product.name,
        "image_url": product.image_url,
        "category": product.category,
      }
    })

  return {
    "id": order.id,
    "status": order.status,
    "total_price": order.total_price,
    "address": order.address,
    "phone": order.phone,
    "created_at": order.created_at,
    "items": items
  }

@router.post("/{order_id}/cancel")
def cancel_order(
  order_id: int,
  current_user=Depends(get_current_user),
  db: Session = Depends(get_db)
):

  order = db.query(Order).filter(
    Order.id == order_id,
    Order.user_id == current_user.id
  ).first()

  if not order:
    raise HTTPException(
      status_code=404,
      detail="Order not found"
    )

  if order.status != "pending":
    raise HTTPException(
      status_code=400,
      detail="Order already processing"
    )

  order.status = "cancelled"

  db.commit()

  return {
    "message": "Order cancelled"
  }