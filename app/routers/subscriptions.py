from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Toy, ToyAllocation, UserCategory
import random
from typing import List
from datetime import datetime

router = APIRouter(
    prefix="/subscriptions",
    tags=["subscriptions"]
)
@router.post("/subscribe/{user_id}")
def subscribe_user(user_id: int, db: Session = Depends(get_db)):
    # Step 1: Fetch the user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Step 2: Check if user already has toys
    active_allocations = db.query(ToyAllocation).filter(
        ToyAllocation.user_id == user_id,
        ToyAllocation.returned_at == None  # Toys not returned yet
    ).count()

    if active_allocations > 0:
        raise HTTPException(status_code=400, detail="User must return toys before subscribing again")

    # Step 3: Fetch the user's preferred categories
    preferred_categories = db.query(UserCategory.category).filter(
        UserCategory.user_id == user_id
    ).all()
    preferred_categories = [c[0] for c in preferred_categories]

    # Step 4: Fetch available toys
    available_toys = db.query(Toy).filter(
        Toy.age_group == user.age_group,  # Match user's age group
        Toy.category.in_(preferred_categories),  # Match preferred categories
        Toy.availability_stat == True  # Toy must be available
    ).limit(5).all()

    if len(available_toys) < 5:
        raise HTTPException(status_code=400, detail="Not enough toys available to subscribe")

    # Step 5: Allocate toys to the user
    current_time = datetime.utcnow()
    for toy in available_toys:
        allocation = ToyAllocation(
            user_id=user.id, 
            toy_id=toy.id,
            assigned_at=current_time
        )
        db.add(allocation)
        toy.availability_stat = False  # Mark toy as unavailable

    db.commit()
    return {"message": f"User {user.name} has been subscribed with {len(available_toys)} toys"}

@router.get("/status/{user_id}")
def check_subscription_status(user_id: int, db: Session = Depends(get_db)):
    active_allocations = db.query(ToyAllocation).filter(
        ToyAllocation.user_id == user_id,
        ToyAllocation.returned_at == None  # Toys not returned
    ).count()

    return {"is_subscribed": active_allocations > 0}