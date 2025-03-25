from db import initialize_db
from fastapi import FastAPI
from routes import categories, expenses, expenses_stats, users

app = FastAPI()

initialize_db()

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(expenses.router, prefix="/expenses", tags=["Expenses"])
app.include_router(expenses_stats.router, prefix="/expenses_stats", tags=["ExpensesStats"])


@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI Banking App"}
