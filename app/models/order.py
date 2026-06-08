from sqlalchemy import (
  Column,
  Integer,
  Float,
  String,
  ForeignKey,
  DateTime
)

from sqlalchemy.orm import relationship

items = relationship(
  "OrderItem",
  backref="order"
)

from datetime import datetime

from app.database import Base

class Order(Base):
  __tablename__ = "orders"

  id = Column(Integer, primary_key=True)
  user_id = Column(Integer, ForeignKey("users.id"))
  total_price = Column(Float)
  address = Column(String)
  phone = Column(String)
  created_at = Column(
    DateTime,
    default=datetime.utcnow
  )
  status = Column(
    String,
    default="pending"
  )