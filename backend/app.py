from fastapi import FastAPI

app = FastAPI(
    title="Smart Inventory SaaS"
)

@app.get("/")
def home():
    return {
        "message": "Smart Inventory SaaS Running"
    }

@app.get("/health")
def health():
    return {
        "status": "ok"
    }
