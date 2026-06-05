from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Business(Base):
   __tablename__="businesses"

   id = Column(Integer, primary_key=True)
   name = Column(String)
   owner = Column(String)
   email = Column(String)
