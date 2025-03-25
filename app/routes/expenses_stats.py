from datetime import datetime, timedelta
from enum import Enum

from auth import get_current_user
from db import Expense, User, get_db
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from routes.expenses import ExpenseResponse


class ExpensePeriod(str, Enum):
    month = "month"
    quarter = "quarter"
    year = "year"


class ExpenseStatsResponse(BaseModel):
    period: str
    total_spent: float


router = APIRouter()


@router.get("/filter", response_model=list[ExpenseResponse])
def filter_expenses(
    category_id: int = None,
    min_amount: float = None,
    max_amount: float = None,
    start_date: str = None,
    end_date: str = None,
    description: str = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Filter expenses based on category, amount range, date range, and description.
    """
    query = db.query(Expense).filter(Expense.user_id == user.id)

    if category_id:
        query = query.filter(Expense.category_id == category_id)
    if min_amount is not None:
        query = query.filter(Expense.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(Expense.amount <= max_amount)
    if start_date:
        try:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.filter(Expense.created_at >= start_date_obj)
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Invalid start_date format. Use YYYY-MM-DD."
            )
    if end_date:
        try:
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
            query = query.filter(Expense.created_at <= end_date_obj)
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Invalid end_date format. Use YYYY-MM-DD."
            )
    if description:
        query = query.filter(Expense.description.ilike(f"%{description}%"))

    expenses = query.all()

    return [ExpenseResponse.from_expense(exp) for exp in expenses]


@router.get("/stats", response_model=ExpenseStatsResponse)
def expense_statistics(
    period: ExpensePeriod = ExpensePeriod.month,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Get money spent & earned in the last month, quarter, or year.
    """
    now = datetime.now()

    if period == ExpensePeriod.month:
        start_date = now - timedelta(days=30)
    elif period == ExpensePeriod.quarter:
        start_date = now - timedelta(days=90)
    elif period == ExpensePeriod.year:
        start_date = now - timedelta(days=365)

    total_spent = (
        db.query(func.sum(Expense.amount))
        .filter(Expense.user_id == user.id, Expense.created_at >= start_date)
        .scalar()
        or 0
    )

    return ExpenseStatsResponse(period=period, total_spent=total_spent)
