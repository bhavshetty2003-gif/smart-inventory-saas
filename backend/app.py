from fastapi import FastAPI, Depends
from backend.schemas.business import BusinessCreate
from backend.database.db import SessionLocal
from backend.models.business import Business
from backend.schemas.product import ProductCreate
from backend.models.product import Product
from backend.schemas.invoice import InvoiceCreate
from backend.models.invoice import Invoice
from backend.models.user import User
from backend.schemas.user import UserCreate
from backend.schemas.login import LoginRequest
from backend.security import hash_password
from backend.security import verify_password
from backend.auth import create_access_token
from backend.dependencies import get_current_user
from backend.database.db import Base, engine

app = FastAPI(
    title="Smart Inventory SaaS"
)
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {
        "message": "Smart Inventory SaaS Running"
    }

@app.post("/businesses")
def create_business(business:BusinessCreate,user=Depends(get_current_user)):

    db= SessionLocal()

    new_business = Business(
        name=business.name,
        owner=business.owner,
        email=business.email,
        owner_id=user["id"]
    )

    db.add(new_business)
    db.commit()

    return {
        "message": "Business saved successfully"
    }
@app.get("/businesses")
def get_businesses(user=Depends(get_current_user)):
    db = SessionLocal()

    businesses = db.query(Business).filter(
        Business.owner_id == user["id"]
    ).all()

    return businesses

@app.delete("/businesses/{business_id}")
def delete_business(
    business_id: int,
    user=Depends(get_current_user)
):
    db = SessionLocal()

    business = db.query(Business).filter(
        Business.id == business_id,
        Business.owner_id == user["id"]
    ).first()

    if not business:
        return {"message": "Business not found"}

    db.delete(business)
    db.commit()

    return {"message": "Business deleted successfully"}
@app.post("/products")
def create_product(product: ProductCreate,user=Depends(get_current_user)):

    db = SessionLocal()

    new_product = Product(
        name=product.name,
        price=product.price,
        owner_id=user["id"],
        quantity=product.quantity
    )

    db.add(new_product)
    db.commit()

    return {
        "message": "Product saved successfully"
    }
@app.get("/products")
def get_products(user=Depends(get_current_user)):
    db = SessionLocal()

    products = db.query(Product).filter(
        Product.owner_id == user["id"]
    ).all()

    return products
@app.put("/products/{product_id}")
def update_product(
    product_id: int,
    product: ProductCreate,
    user=Depends(get_current_user)
):
    db = SessionLocal()

    existing_product = db.query(Product).filter(
        Product.id == product_id,
        Product.owner_id == user["id"]
    ).first()

    if not existing_product:
        return {"message": "Product not found"}

    existing_product.name = product.name
    existing_product.price = product.price
    existing_product.quantity = product.quantity

    db.commit()

    return {"message": "Product updated successfully"}
@app.post("/invoices")
def create_invoice(invoice: InvoiceCreate,user=Depends(get_current_user)):

    db = SessionLocal()

    product = db.query(Product).filter(
        Product.id == invoice.product_id
    ).first()

    if not product:
        return {"message": "Product not found"}

    if product.quantity < invoice.quantity:
        return {"message": "Insufficient stock"}

    total_amount = product.price * invoice.quantity

    product.quantity -= invoice.quantity

    new_invoice = Invoice(
        product_id=invoice.product_id,
        quantity=invoice.quantity,
        total_amount=total_amount,
        owner_id=user["id"]
    )

    db.add(new_invoice)
    db.commit()
    return {
        "message": "Invoice saved successfully"
    }

@app.get("/invoices")
def get_invoices(user=Depends(get_current_user)):

    db = SessionLocal()

    invoices = db.query(Invoice).filter(
        Invoice.owner_id == user["id"]
    ).all()

    return invoices

@app.get("/dashboard")
def dashboard(user=Depends(get_current_user)):

    db = SessionLocal()

    total_products = db.query(Product).filter(
        Product.owner_id == user["id"]
    ).count()

    total_invoices = db.query(Invoice).filter(
        Invoice.owner_id == user["id"]
    ).count()

    total_businesses = db.query(Business).filter(
        Business.owner_id == user["id"]
    ).count()

    total_revenue = sum(
        invoice.total_amount
        for invoice in db.query(Invoice).all()
    )

    return {
        "total_products": total_products,
        "total_invoices": total_invoices,
        "total_revenue": total_revenue,
        "businesses": total_businesses,
    }
@app.post("/register")
def register(user: UserCreate):

    db = SessionLocal()

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        return {
            "message": "Email already exists"
        }
    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()

    return {
        "message": "User registered successfully"
    }
@app.post("/login")
def login(login_data: LoginRequest):

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == login_data.email
    ).first()

    if not user:
        return {"message": "User not found"}

    if not verify_password(
        login_data.password,
        user.password
    ):
        return {"message": "Invalid password"}

    token = create_access_token(
        {"email": user.email}
    )

    return {
        "access_token": token
    }

@app.get("/me")
def get_me(user=Depends(get_current_user)):
    return user

@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    user=Depends(get_current_user)
):
    db = SessionLocal()

    product = db.query(Product).filter(
        Product.id == product_id,
        Product.owner_id == user["id"]
    ).first()

    if not product:
        return {"message": "Product not found"}

    db.delete(product)
    db.commit()

    return {"message": "Product deleted"}
@app.put("/businesses/{business_id}")
def update_business(
    business_id: int,
    business: BusinessCreate,
    user=Depends(get_current_user)
):
    db = SessionLocal()

    existing_business = db.query(Business).filter(
        Business.id == business_id,
        Business.owner_id == user["id"]
    ).first()

    if not existing_business:
        return {"message": "Business not found"}

    existing_business.name = business.name
    existing_business.owner = business.owner
    existing_business.email = business.email

    db.commit()

    return {"message": "Business updated successfully"}
@app.put("/invoices/{invoice_id}")
def update_invoice(
    invoice_id: int,
    invoice: InvoiceCreate,
    user=Depends(get_current_user)
):
    db = SessionLocal()

    existing_invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id,
        Invoice.owner_id == user["id"]
    ).first()

    if not existing_invoice:
        return {"message": "Invoice not found"}

    existing_invoice.product_id = invoice.product_id
    existing_invoice.quantity = invoice.quantity

    db.commit()

    return {"message": "Invoice updated successfully"}

@app.delete("/invoices/{invoice_id}")
def delete_invoice(
    invoice_id: int,
    user=Depends(get_current_user)
):
    db = SessionLocal()

    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id,
        Invoice.owner_id == user["id"]
    ).first()

    if not invoice:
        return {"message": "Invoice not found"}

    db.delete(invoice)
    db.commit()

    return {"message": "Invoice deleted successfully"}

@app.get("/dashboard/revenue")
def revenue_dashboard(
    user=Depends(get_current_user)
):
    db = SessionLocal()

    invoices = db.query(Invoice).filter(
        Invoice.owner_id == user["id"]
    ).all()

    total_revenue = sum(invoice.total_amount for invoice in invoices)

    for invoice in invoices:
        total_revenue += invoice.total_amount

    return {
        "total_revenue": total_revenue,
        "total_invoices": len(invoices)
    }
@app.get("/dashboard/low-stock")
def low_stock_dashboard(
    user=Depends(get_current_user)
):
    db = SessionLocal()

    products = db.query(Product).filter(
        Product.owner_id == user["id"],
        Product.quantity < 5
    ).all()

    return {
        "low_stock_products": products,
        "count": len(products)
    }
@app.get("/dashboard/summary")
def dashboard_summary(
    user=Depends(get_current_user)
):
    db = SessionLocal()

    products = db.query(Product).filter(
        Product.owner_id == user["id"]
    ).all()

    businesses = db.query(Business).filter(
        Business.owner_id == user["id"]
    ).all()

    invoices = db.query(Invoice).filter(
        Invoice.owner_id == user["id"]
    ).all()

    total_revenue = sum(
        invoice.total_amount for invoice in invoices
    )

    low_stock_count = len([
        product for product in products
        if product.quantity < 5
    ])

    return {
        "total_products": len(products),
        "total_businesses": len(businesses),
        "total_invoices": len(invoices),
        "total_revenue": total_revenue,
        "low_stock_count": low_stock_count
    }
@app.get("/ai/recommendations")
def ai_recommendations(
    user=Depends(get_current_user)
):
    db = SessionLocal()

    products = db.query(Product).filter(
        Product.owner_id == user["id"]
    ).all()

    recommendations = []

    for product in products:
        if product.quantity < 5:
            recommendations.append({
                "product": product.name,
                "current_stock": product.quantity,
                "recommendation": f"Reorder {20 - product.quantity} units"
            })

    return {
        "recommendations": recommendations
    }
@app.get("/ai/average-sales")
def average_sales(
    user=Depends(get_current_user)
):
    db = SessionLocal()

    invoices = db.query(Invoice).filter(
        Invoice.owner_id == user["id"]
    ).all()

    total_quantity = sum(
        invoice.quantity for invoice in invoices
    )

    days = 30

    return {
        "average_daily_sales":
        round(total_quantity / days, 2)
    }
@app.get("/ai/stockout-prediction")
def stockout_prediction(
    user=Depends(get_current_user)
):
@app.get("/ai/insights")
def ai_insights(
    user=Depends(get_current_user)
):
