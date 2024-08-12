from fastapi import FastAPI
from app.routers import customer

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello, World!"}

app.include_router(customer.router)