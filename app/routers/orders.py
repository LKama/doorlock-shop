from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.cart_item import CartItem
from app.models.order import Order
from app.models.order_item import OrderItem

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
  background_tasks: BackgroundTasks,
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
    phone=phone
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

  print("ABOUT TO SEND EMAIL TASK")

  background_tasks.add_task(
    send_order_email,
    current_user.email,
    order.id
)

  print("EMAIL TASK ADDED")

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