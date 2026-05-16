from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database import get_db

from app.models.cart_item import CartItem
from app.models.product import Product

from app.utils.dependencies import get_current_user

router = APIRouter(
  prefix="/cart",
  tags=["Cart"]
)

@router.get("/")
def get_cart(
  current_user = Depends(get_current_user),
  db: Session = Depends(get_db)
):
  
  items =  db.query(CartItem).options(
    joinedload(CartItem.product)
  ).filter(
    CartItem.user_id == current_user.id
  ).all()

  result = []

  for item in items:
    result.append({
      "id": item.id,
      "quantity": item.quantity,
      "product": {
        "id": item.product.id,
        "name": item.product.name,
        "price": item.product.price,
        "image_url": item.product.image_url,
      }
    })
  
  return result

@router.post("/add")
def add_to_cart(
  product_id: int,
  quantity: int,
  current_user = Depends(get_current_user),
  db: Session = Depends(get_db)
):
  
  product = db.query(Product).filter(
    Product.id == product_id
  ).first()

  if not product:
    raise HTTPException(
      status_code=404,
      detail="Product not found"
    )
  
  existing = db.query(CartItem).filter(
    CartItem.user_id == current_user.id,
    CartItem.product_id == product_id
  ).first()

  if existing:
    existing.quantity += quantity
  else:
    item = CartItem(
      user_id=current_user.id,
      product_id=product_id,
      quantity=quantity
    )

    db.add(item)
  
  db.commit()

  return {"message": "Added to cart"}

@router.delete("/remove")
def remove_from_cart(
  item_id: int,
  current_user = Depends(get_current_user),
  db: Session = Depends(get_db)
):
  
  item = db.query(CartItem).filter(
    CartItem.id == item_id,
    CartItem.user_id == current_user.id
  ).first()

  if not item:
    raise HTTPException(
      status_code=404,
      detail="Item not found"
    )
  
  db.delete(item)

  db.commit()

  return {"message": "Removed"}

@router.put("/update")
def update_cart(
  item_id: int,
  quantity: int,
  current_user = Depends(get_current_user),
  db: Session = Depends(get_db)
):
  
  item = db.query(CartItem).filter(
    CartItem.id == item_id,
    CartItem.user_id == current_user.id
  ).first()

  if not item:
    raise HTTPException(
      status_code=404,
      detail="Item not found"
    )
  
  item.quantity = quantity

  db.commit()

  return {"message": "Updated"}