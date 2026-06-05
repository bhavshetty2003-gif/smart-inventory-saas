from backend.database.db import engine, Base
from backend.models.business import Business

Base.metadata.create_all(bind=engine)

print("Tables created successfully!")
