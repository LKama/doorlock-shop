from sqlalchemy import Column, Integer, String, Float, Text, JSON
from app.database import Base

class Product(Base):
  __tablename__ = "products"

  id = Column(Integer, primary_key=True, index=True)

  name = Column(String, nullable=False)

  description = Column(String, nullable=False)

  price = Column(Float, nullable=False)

  category = Column(String, nullable=False)

  image_url = Column(String, nullable=False)

  stock = Column(Integer, default=0)

  specifications = Column(JSON, default={}, nullable=True)