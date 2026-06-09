from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    price: float
    quantity: int
    business_id : int
