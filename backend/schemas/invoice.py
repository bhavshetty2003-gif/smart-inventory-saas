from pydantic import BaseModel

class InvoiceCreate(BaseModel):
    product_id: int
    quantity: int
