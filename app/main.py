from db import initialize_db
from fastapi import FastAPI
from routes import users

from routes import categories, expenses

app = FastAPI()

initialize_db()

# Include routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(expenses.router, prefix="/expenses", tags=["Expenses"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])


@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI Banking App"}
