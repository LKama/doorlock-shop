from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.auth import Token
from app.schemas.login import LoginRequest
from app.utils.dependencies import get_current_user
from app.utils.security import(
  hash_password,
  verify_password,
  create_access_token
)

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", operation_id="auth_register")
def register(user: UserCreate, db: Session = Depends(get_db)):

  exiting_user = db.query(User).filter(
    User.email == user.email
  ).first()

  if exiting_user:
    raise HTTPException(
      status_code=400,
      detail="Email alredy exists"
    )
  
  new_user = User(
    email=user.email,
    password_hash=hash_password(user.password),
    name=user.name
  )

  db.add(new_user)
  db.commit()

  return {"message": "User created"}

@router.post("/login", response_model=Token, operation_id="auth_login")
def login(
    user: LoginRequest,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        user.password,
        db_user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token({
        "sub": str(db_user.id)
    })
    print(token)

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me")
def get_me(
   current_user = Depends(get_current_user)
):
   
   return {
      "id": current_user.id,
      "email": current_user.email,
      "name": current_user.name,
   }