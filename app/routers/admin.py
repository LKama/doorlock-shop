from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from fastapi import UploadFile, File, Form
from fastapi.responses import RedirectResponse
import shutil
import os

from app.database import get_db
from app.models.user import User
from app.models.product import Product
from app.models.order import Order

router = APIRouter()

templates = Jinja2Templates(
  directory="templates"
)


@router.get("/admin")
def admin_dashboard(
  request: Request,
  db: Session = Depends(get_db)
):

  users_count = db.query(User).count()

  products_count = db.query(Product).count()

  orders_count = db.query(Order).count()

  recent_orders = (
    db.query(Order)
    .order_by(Order.id.desc())
    .limit(10)
    .all()
  )

  return templates.TemplateResponse(
    "admin/dashboard.html",
    {
      "request": request,
      "users_count": users_count,
      "products_count": products_count,
      "orders_count": orders_count,
      "recent_orders": recent_orders
    }
  )


@router.get("/admin/products")
def admin_products(
    request: Request,
    db: Session = Depends(get_db)
):

  products = db.query(Product).all()

  return templates.TemplateResponse(
    "admin/products.html",
    {
      "request": request,
      "products": products
    }
  )


@router.get("/admin/orders")
def admin_orders(
  request: Request,
  db: Session = Depends(get_db)
):

  orders = db.query(Order).all()

  return templates.TemplateResponse(
    "admin/orders.html",
    {
      "request": request,
      "orders": orders
    }
  )


@router.get("/admin/users")
def admin_users(
  request: Request,
  db: Session = Depends(get_db)
):

  users = db.query(User).all()

  return templates.TemplateResponse(
    "admin/users.html",
    {
    "request": request,
    "users": users
    }
  )

@router.post("/admin/products/create")
def create_product(
  name: str = Form(...),
  description: str = Form(...),
  price: float = Form(...),
  category: str = Form(...),
  stock: int = Form(...),
  image: UploadFile = File(...),
  db: Session = Depends(get_db)
):

  filename = image.filename

  filepath = f"static/uploads/{filename}"

  with open(filepath, "wb") as buffer:
    shutil.copyfileobj(image.file, buffer)

  product = Product(
    name=name,
    description=description,
    price=price,
    category=category,
    stock=stock,
    image_url=f"/static/uploads/{filename}"
  )

  db.add(product)
  db.commit()

  return RedirectResponse(
    "/admin/products",
    status_code=303
  )

@router.get("/admin/products/new")
def new_product_page(
  request: Request
):
  return templates.TemplateResponse(
    "admin/product_form.html",
    {
      "request": request
    }
  )

@router.get(
  "/admin/products/{product_id}/edit"
)
def edit_product_page(
  product_id: int,
  request: Request,
  db: Session = Depends(get_db)
):

  product = db.query(Product).get(product_id)

  return templates.TemplateResponse(
    "admin/edit_product.html",
    {
      "request": request,
      "product": product
    }
  )

@router.post(
  "/admin/products/{product_id}/edit"
)
def edit_product(
  product_id: int,
  name: str = Form(...),
  description: str = Form(...),
  price: float = Form(...),
  category: str = Form(...),
  stock: int = Form(...),
  db: Session = Depends(get_db)
):

  product = db.query(Product).get(product_id)

  product.name = name
  product.description = description
  product.price = price
  product.category = category
  product.stock = stock

  db.commit()

  return RedirectResponse(
    "/admin/products",
    status_code=303
  )

@router.post(
  "/admin/orders/{order_id}/status"
)
def change_order_status(
  order_id: int,
  status: str = Form(...),
  db: Session = Depends(get_db)
):

  order = db.query(Order).get(order_id)

  order.status = status

  db.commit()

  return RedirectResponse(
    "/admin/orders",
    status_code=303
  )

@router.post(
  "/admin/products/{product_id}/delete"
)
def delete_product(
  product_id: int,
  db: Session = Depends(get_db)
):

  product = db.query(Product).get(product_id)

  db.delete(product)

  db.commit()

  return RedirectResponse(
    "/admin/products",
    status_code=303
)