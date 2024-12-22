from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
import logging
from fastapi.responses import JSONResponse

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("")
async def get_users(db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()
        print(f"Found users: {users}")
        return [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
            }
            for user in users
        ]
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test")
async def create_test_user(db: Session = Depends(get_db)):
    test_user = User(
        name="Test User",
        email="test@example.com"
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    return test_user