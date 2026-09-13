from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="PharmaSync",
    description="Pharmaceutical Inventory Management System",
    version="1.0.0"
)

app.include_router(router)

@app.get("/health")
def health_check():
    return {
        "status": "ok", 
        "app": "PharmaSync"
    }