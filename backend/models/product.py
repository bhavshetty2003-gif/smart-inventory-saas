from sqlalchemy import Column, Integer, String, Float
from backend.database.db import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    owner_id = Column(Integer)
