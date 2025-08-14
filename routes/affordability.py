from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
import schemas, models, auth, database
from typing import List
router = APIRouter(prefix="/affordability", tags=["Affordability"])

