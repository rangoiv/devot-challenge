from typing import List

from db import ExpenseCategory, get_db
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session


class CategoryCreate(BaseModel):
    name: str


class CategoryResponse(CategoryCreate):
    id: int

    class Config:
        from_attributes = True


router = APIRouter()


@router.post("/", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = (
        db.query(ExpenseCategory).filter(ExpenseCategory.name == category.name).first()
    )
    if db_category:
        raise HTTPException(status_code=400, detail="Category already exists")
    new_category = ExpenseCategory(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.get("/", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(ExpenseCategory).all()


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = (
        db.query(ExpenseCategory).filter(ExpenseCategory.id == category_id).first()
    )
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int, updated_category: CategoryCreate, db: Session = Depends(get_db)
):
    category = (
        db.query(ExpenseCategory).filter(ExpenseCategory.id == category_id).first()
    )
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category.name = updated_category.name
    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = (
        db.query(ExpenseCategory).filter(ExpenseCategory.id == category_id).first()
    )
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}
