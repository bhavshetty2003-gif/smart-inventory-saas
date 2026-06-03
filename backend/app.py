from fastapi import FastAPI 

app = FastAPI(
    title = "Smart_inventory_Saas"
)

@app.get("/")
def home():
    return {
"message":"Smart_inventory_Saas Running"
}
