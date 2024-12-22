from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Toy

router = APIRouter()

@router.get("/toys")
def get_toys(db: Session = Depends(get_db)):
    toys = db.query(Toy).all()
    return toys