from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User

from app.config import SECRET_KEY, ALGORITHM

security = HTTPBearer()

def get_current_user(
  credentials: HTTPAuthorizationCredentials = Depends(security),
  db: Session = Depends(get_db)
):
  
  token = credentials.credentials
  

  try:
    payload = jwt.decode(
      token,
      SECRET_KEY,
      algorithms=[ALGORITHM]
    )

    user_id = int(payload.get("sub"))
  
  except Exception as e:
    print(e)
    raise HTTPException(
        status_code=401,
        detail="Invalid token"
    )
  
  user = db.query(User).filter(
    User.id == user_id
  ).first()

  if not user:
    raise HTTPException(
      status_code=401,
      detail="User not found"
    )
  
  return user