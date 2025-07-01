from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.auth.security import SECRET_KEY, ALGORITHM
from app.auth.security import get_current_user
import shutil
import os

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/")
def upload_file(file: UploadFile = File(...), current_user: str = Depends(get_current_user)):
    filename = f"{current_user.email}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": "✅ File uploaded successfully", "filename": filename}
