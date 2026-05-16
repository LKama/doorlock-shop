from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.product import Product

router = APIRouter(
  prefix="/products",
  tags=["Products"]
)

@router.get("/")
def get_products(
  category: str = None,
  search: str = None,
  db: Session = Depends(get_db)
):
  query = db.query(Product)

  if category:
    query = query.filter(
      Product.category == category
    )

  if search:
    query = query.filter(
      Product.name.ilike(f"%{search}%")
    )

  return query.all()

@router.get("/{product_id}")
def get_product(
  product_id: int,
  db: Session = Depends(get_db)
):
  
  return db.query(Product).filter(
    Product.id == product_id
  ).first()