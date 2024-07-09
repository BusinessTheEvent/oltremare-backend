from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.auth.models import User
from src.databases.db import get_db
from src.default_logger import get_custom_logger


router = APIRouter()
logger = get_custom_logger(__name__)

@router.get("/")
def healtcheck():
    return {"status": "ok", "version": "0.1"}

#accessibile solo da admin
@router.get("/users/all")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
    
