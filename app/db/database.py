from env import env
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .base import Base
from .model import ExpenseCategory

engine = create_engine(env["postgres.url"])
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def initialize_db():
    """Create tables and seed predefined categories."""
    db = SessionLocal()
    # db.execute(text("DROP SCHEMA public CASCADE;"))
    # db.execute(text("CREATE SCHEMA public;"))
    # db.commit()
    Base.metadata.create_all(bind=engine)

    predefined_categories = [
        "Food",
        "Transport",
        "Entertainment",
        "Utilities",
        "Health",
    ]

    for name in predefined_categories:
        if not db.query(ExpenseCategory).filter_by(name=name).first():
            db.add(ExpenseCategory(name=name))

    db.commit()
    db.close()
