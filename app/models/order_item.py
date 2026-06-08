from sqlalchemy import (
  Column,
  Integer,
  Float,
  ForeignKey
)

from sqlalchemy.orm import relationship

product = relationship(
  "Product"
)

from app.database import Base

class OrderItem(Base):
  __tablename__ = "order_items"

  id = Column(Integer, primary_key=True)
  order_id = Column(
    Integer,
    ForeignKey("orders.id")
  )
  product_id = Column(
    Integer,
    ForeignKey("products.id")
  )
  quantity = Column(Integer)
  price_at_moment = Column(Float)
