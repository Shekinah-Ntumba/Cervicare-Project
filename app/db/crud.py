# app/db/crud.py
from sqlalchemy.orm import Session
from app.db import models  # make sure models.User exists

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()
