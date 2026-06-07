from sqlalchemy import Column, Integer, String
from backend.database.db import Base

class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    owner = Column(String)
    email = Column(String)
    owner_id = Column(Integer)
