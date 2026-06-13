from fastapi import (
    APIRouter,
    Request,
    Depends,
    UploadFile,
    File,
    Form,
)

from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

import shutil
import os

from app.database import get_db
from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from app.models.chat_message import ChatMessage

router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


# =========================
# DASHBOARD
# =========================

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
        request=request,
        name="admin/dashboard.html",
        context={
            "users_count": users_count,
            "products_count": products_count,
            "orders_count": orders_count,
            "recent_orders": recent_orders,
        }
    )


# =========================
# PRODUCTS
# =========================

@router.get("/admin/products")
def admin_products(
    request: Request,
    db: Session = Depends(get_db)
):

    products = db.query(Product).all()

    return templates.TemplateResponse(
        request=request,
        name="admin/products.html",
        context={
            "products": products
        }
    )


@router.get("/admin/products/new")
def new_product_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="admin/product_form.html",
        context={}
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

    os.makedirs(
        "static/uploads",
        exist_ok=True
    )

    filename = image.filename

    filepath = f"static/uploads/{filename}"

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(
            image.file,
            buffer
        )

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


@router.get(
    "/admin/products/{product_id}/edit"
)
def edit_product_page(
    product_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    return templates.TemplateResponse(
        request=request,
        name="admin/edit_product.html",
        context={
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

    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if product:

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
    "/admin/products/{product_id}/delete"
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):

    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if product:

        db.delete(product)
        db.commit()

    return RedirectResponse(
        "/admin/products",
        status_code=303
    )


# =========================
# ORDERS
# =========================

@router.get("/admin/orders")
def admin_orders(
    request: Request,
    db: Session = Depends(get_db)
):

    orders = (
        db.query(Order)
        .order_by(Order.id.desc())
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="admin/orders.html",
        context={
            "orders": orders
        }
    )


@router.post(
    "/admin/orders/{order_id}/status"
)
def change_order_status(
    order_id: int,
    status: str = Form(...),
    db: Session = Depends(get_db)
):

    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if order:

        order.status = status
        db.commit()

    return RedirectResponse(
        "/admin/orders",
        status_code=303
    )


# =========================
# USERS
# =========================

@router.get("/admin/users")
def admin_users(
    request: Request,
    db: Session = Depends(get_db)
):

    users = (
        db.query(User)
        .order_by(User.id.desc())
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="admin/users.html",
        context={
            "users": users
        }
    )

@router.get("/admin/chat/{user_id}")
def admin_chat(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    user = db.query(User).get(user_id)

    messages = (
        db.query(ChatMessage)
        .filter(
            ChatMessage.user_id == user_id
        )
        .order_by(
            ChatMessage.created_at.asc()
        )
        .all()
    )

    return templates.TemplateResponse(
        "admin/chat.html",
        {
            "request": request,
            "user": user,
            "messages": messages
        }
    )

@router.post("/admin/chat/{user_id}")
def admin_send_message(
    user_id: int,
    message: str = Form(...),
    db: Session = Depends(get_db)
):

    msg = ChatMessage(
        user_id=user_id,
        sender="admin",
        message=message
    )

    db.add(msg)

    db.commit()

    return RedirectResponse(
        f"/admin/chat/{user_id}",
        status_code=303
    )