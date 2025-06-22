from fastapi import FastAPI
from app.routes import  predict, upload
from app.auth import routes as auth_routes
from dotenv import load_dotenv
import os

load_dotenv()


app = FastAPI (
     title= os.getenv("title"),
     description = os.getenv("description"),
     version = os.getenv("version")
)
app.include_router(predict.router, prefix="/predict", tags=["Prediction"])
app.include_router(upload.router, prefix="/upload", tags=["File Upload"])
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])

from app.routes import resources

app.include_router(resources.router)
from fastapi.staticfiles import StaticFiles
import os

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

