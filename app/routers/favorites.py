from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.favorite import Favorite
from app.models.product import Product

from app.utils.dependencies import get_current_user

router = APIRouter(
    prefix="/favorites",
    tags=["Favorites"]
)

@router.get("/")
def get_favorites(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    favorites = db.query(Favorite).filter(
        Favorite.user_id == current_user.id
    ).all()

    result = []

    for fav in favorites:

        product = db.query(Product).filter(
            Product.id == fav.product_id
        ).first()

        if product:

            result.append({
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "category": product.category,
                "image_url": product.image_url,
                "specifications": product.specifications,
                "stock": product.stock,
            })

    return result

@router.post("/toggle")
def toggle_favorite(
    data: dict,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    product_id = data["product_id"]

    favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.product_id == product_id
    ).first()

    if favorite:

        db.delete(favorite)

        db.commit()

        return {
            "message": "removed"
        }

    favorite = Favorite(
        user_id=current_user.id,
        product_id=product_id
    )

    db.add(favorite)

    db.commit()

    return {
        "message": "added"
    }

@router.get("/test")
def test():
    return {"ok": True}