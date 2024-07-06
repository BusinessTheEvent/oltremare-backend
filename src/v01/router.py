from fastapi import APIRouter

from src.default_logger import get_custom_logger


router = APIRouter()
logger = get_custom_logger(__name__)

@router.get("/")
def healtcheck():
    return {"status": "ok", "version": "0.1"}

