from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.auth.security import SECRET_KEY, ALGORITHM
from app.services.model_service import run_batch_prediction
from app.services.pdf_service import generate_pdf_report
import os

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        if user_email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/")
def predict_from_uploaded_file(current_user: str = Depends(get_current_user)):
    # Find user file
    upload_dir = "uploads"
    filename = None
    for f in os.listdir(upload_dir):
        if f.startswith(current_user):
            filename = f
            break

    if not filename:
        raise HTTPException(status_code=404, detail="No uploaded file found for user.")

    file_path = os.path.join(upload_dir, filename)

    # Predict
    predictions = run_batch_prediction(file_path)

    # Generate PDF
    pdf_path = generate_pdf_report(current_user, predictions)

    return {
        "message": "✅ Prediction complete.",
        "pdf_report": pdf_path,
        "links": {
            "book_screening": "/screening/book",
            "estimate_treatment": "/treatment/estimate",
            "healthcare_institutions": "/resources/healthcare",
            "financial_support": "/resources/financial"
        }
    }
