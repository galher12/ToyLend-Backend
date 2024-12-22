print("Starting to load main.py...")

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, get_db
from app.models import Base  # Import Base from models, not database
from app.routers import toys, users, subscriptions, returns

print("Imports successful")

app = FastAPI()
print("FastAPI app created")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(toys.router)
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(subscriptions.router, prefix="/api/subscriptions", tags=["subscriptions"])
app.include_router(returns.router, prefix="/api/returns", tags=["returns"])

# Basic health check endpoint
@app.get("/")
async def root():
    return {"status": "healthy"}

@app.get("/api/subscriptions/status/{user_id}")
async def get_subscription_status(user_id: int):
    subscription = await get_db().fetch_one(
        "SELECT * FROM subscriptions WHERE user_id = :user_id AND is_active = TRUE",
        {"user_id": user_id}
    )
    
    return {"is_subscribed": subscription is not None}

@app.post("/api/subscriptions/subscribe/{user_id}")
async def subscribe_user(user_id: int):
    try:
        # Add your subscription logic here
        # For example:
        subscription = await get_db().execute(
            """
            INSERT INTO subscriptions (user_id, is_active, created_at)
            VALUES (:user_id, TRUE, CURRENT_TIMESTAMP)
            """,
            {"user_id": user_id}
        )
        return {"message": "Successfully subscribed", "user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/subscriptions")  # or whatever your route is
async def create_subscription(user_id: int, db = Depends(get_db)):
    subscription = db.execute(
        """
        INSERT INTO subscriptions (user_id, is_active, created_at)
        """
    )
