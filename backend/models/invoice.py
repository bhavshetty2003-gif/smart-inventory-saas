from sqlalchemy import Column, Integer, Float, DateTime
from backend.database.db import Base
from datetime import datetime

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    quantity = Column(Integer)
    total_amount = Column(Float)
    owner_id = Column(Integer)

    invoice_date = Column(
        DateTime,
        default=datetime.utcnow
    )
