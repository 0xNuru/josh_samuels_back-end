from fastapi import FastAPI
from app.routers import customer, auth, product, payment
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://joshsamuels.co",
        "https://www.joshsamuels.co",
        "https://dev.joshsamuels.co",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def hello():
    return {"message": "Hello, World!"}


app.include_router(auth.router)
app.include_router(customer.router)
app.include_router(product.router)
app.include_router(payment.router)
