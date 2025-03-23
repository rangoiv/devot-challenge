from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
from model import User
from schema import UserCreate, Token
from auth import hash_password, verify_password, create_access_token
from datetime import timedelta

router = APIRouter()

@router.post("/register/", response_model=Token)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(email=user_data.email, hashed_password=hash_password(user_data.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(data={"sub": new_user.email}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login/", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}
