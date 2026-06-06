from backend.database.db import engine, Base
from backend.models.business import Business
from backend.models.product import Product
from backend.models.invoice import Invoice
from backend.models.user import User

Base.metadata.create_all(bind=engine)

print("Tables created successfully!")
