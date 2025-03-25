from typing import Optional

from auth import get_current_user
from db import Expense, ExpenseCategory, User, get_db
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session


class ExpenseCreate(BaseModel):
    description: str
    amount: float
    category_id: int


class ExpenseUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None
    category_id: Optional[int] = None


class ExpenseCategoryResponse(BaseModel):
    id: int
    name: str


class ExpenseResponse(BaseModel):
    id: int
    description: str
    amount: float
    category: ExpenseCategoryResponse

    @staticmethod
    def from_expense(expense: Expense):
        return ExpenseResponse(
            id=expense.id,
            description=expense.description,
            amount=expense.amount,
            category={"id": expense.category.id, "name": expense.category.name},
        )


router = APIRouter()


@router.post("/", response_model=ExpenseResponse)
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Create a new expense."""
    category = (
        db.query(ExpenseCategory)
        .filter(ExpenseCategory.id == expense.category_id)
        .first()
    )
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    new_expense = Expense(
        user_id=user.id,
        category_id=expense.category_id,
        amount=expense.amount,
        description=expense.description,
    )
    user.balance -= new_expense.amount

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return ExpenseResponse.from_expense(new_expense)


@router.get("/", response_model=list[ExpenseResponse])
def get_expenses(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Retrieve all expenses for the authenticated user."""
    expenses = db.query(Expense).filter(Expense.user_id == user.id).all()
    return [ExpenseResponse.from_expense(exp) for exp in expenses]


@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Retrieve a single expense."""
    expense = (
        db.query(Expense)
        .filter(Expense.id == expense_id, Expense.user_id == user.id)
        .first()
    )
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    return ExpenseResponse.from_expense(expense)


@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    expense_update: ExpenseUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Update an existing expense."""
    expense = (
        db.query(Expense)
        .filter(Expense.id == expense_id, Expense.user_id == user.id)
        .first()
    )
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    if expense_update.description:
        expense.description = expense_update.description
    if expense_update.amount:
        user.balance = user.balance - expense_update.amount + expense.amount
        expense.amount = expense_update.amount
    if expense_update.category_id:
        category = (
            db.query(ExpenseCategory)
            .filter(ExpenseCategory.id == expense_update.category_id)
            .first()
        )
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        expense.category_id = category.id

    db.commit()
    db.refresh(expense)

    return ExpenseResponse.from_expense(expense)


@router.delete("/{expense_id}", response_model=dict)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Delete an expense by ID."""
    expense = (
        db.query(Expense)
        .filter(Expense.id == expense_id, Expense.user_id == user.id)
        .first()
    )
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    user.balance = user.balance + expense.amount
    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted successfully"}
