from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models import User, Toy, ToyAllocation

router = APIRouter(
    prefix="/returns",
    tags=["returns"]
)
@router.post("/return/{user_id}")
def return_toys(user_id: int, db: Session = Depends(get_db)):
    # Fetch active allocations
    allocations = db.query(ToyAllocation).filter(
        ToyAllocation.user_id == user_id,
        ToyAllocation.returned_at == None
    ).all()

    if not allocations:
        raise HTTPException(status_code=400, detail="User has no active toys to return")

    # Mark toys as returned
    for allocation in allocations:
        allocation.returned_at = datetime.utcnow()
        toy = db.query(Toy).filter(Toy.id == allocation.toy_id).first()
        toy.availability_stat = True  # Mark toy as available

    db.commit()
    return {"message": f"User {user_id} has returned {len(allocations)} toys"}