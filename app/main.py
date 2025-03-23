from fastapi import FastAPI
from database import engine, Base
from routes import users, transactions

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])

@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI Banking App"}
