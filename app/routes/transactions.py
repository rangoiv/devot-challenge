from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from model import User, Transaction
from schema import TransactionRequest
from auth import get_current_user

router = APIRouter()

@router.post("/deposit/")
def deposit(amount: TransactionRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if amount.amount <= 0:
        raise HTTPException(status_code=400, detail="Deposit amount must be positive")

    current_user.balance += amount.amount
    db.commit()

    new_transaction = Transaction(user_id=current_user.id, amount=amount.amount)
    db.add(new_transaction)
    db.commit()

    return {"message": f"Deposited {amount.amount}. New balance: {current_user.balance}"}

@router.get("/balance/")
def get_balance(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return {"balance": current_user.balance}
