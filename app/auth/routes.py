from  fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import database, models
from app.models import user_schema
from app.auth.security import get_password_hash, verify_password, create_access_token
router = APIRouter()
#Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.post("/register", response_model=user_schema.UserOut)
def register(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return user_schema.UserOut(id=new_user.id, email=new_user.email)  # ✅ FIXED LINE


# @router.post("/login")
# def login(user: user_schema.UserLogin, db: Session= Depends(get_db)):
#     db_user = db.query(models.User).filter(models.User.email == user.email).first()
#     if not db_user or not verify_password( user.password, db_user.hashed_password):
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#         access_token = create_access_token(data={"sub": db_user.email})
#         return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login")
def login(user: user_schema.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}



