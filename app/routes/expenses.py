from auth import get_current_user
from db import Expense, User, get_db
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

router = APIRouter()


class ExpenseRequest(BaseModel):
    amount: float


@router.post("/category/")
def deposit(
    amount: ExpenseRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if amount.amount <= 0:
        raise HTTPException(status_code=400, detail="Deposit amount must be positive")

    current_user.balance += amount.amount
    db.commit()

    new_transaction = Expense(user_id=current_user.id, amount=amount.amount)
    db.add(new_transaction)
    db.commit()

    return {
        "message": f"Deposited {amount.amount}. New balance: {current_user.balance}"
    }


@router.get("/balance/")
def get_balance(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return {"balance": current_user.balance}
