from typing import Annotated, Union
from fastapi import APIRouter, Depends, HTTPException, Request, status

from ..default_logger import get_custom_logger


router = APIRouter()
logger = get_custom_logger(__name__)


## ROUTES ##

@router.get("/new", tags=["Licensing"])
async def new_license(request: Request):
    return {"message": "New license"}


@router.get("/validate", tags=["Licensing"])
async def validate_license(request: Request):
    return {"message": "Validate license"}


@router.get("/renew", tags=["Licensing"])
async def renew_license(request: Request):
    return {"message": "Renew license"}


@router.get("/revoke", tags=["Licensing"])
async def revoke_license(request: Request):
    return {"message": "Revoke license"}
