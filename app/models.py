from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

# Users Table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    address = Column(String)
    phone_number = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    subscriptions = relationship("Subscription", back_populates="user")
    categories = relationship("UserCategory", back_populates="user", cascade="all, delete")
    age_group = Column(String)
    allocations = relationship("ToyAllocation", back_populates="user")

# Toys Table
class Toy(Base):
    __tablename__ = "toys"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    age_group = Column(String)
    condition = Column(String, default="new")
    availability_stat = Column(Boolean, default=True)
    times_rented = Column(Integer, default=0)
    image_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    allocations = relationship("ToyAllocation", back_populates="toy")

# Subscriptions Table
class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    user = relationship("User", back_populates="subscriptions")

# Toy Allocations Table
class ToyAllocation(Base):
    __tablename__ = "toy_allocations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    toy_id = Column(Integer, ForeignKey("toys.id"), nullable=False)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=False)
    returned_at = Column(DateTime, nullable=True)
    assigned_at = Column(DateTime, nullable=True)
    user = relationship("User", back_populates="allocations")
    toy = relationship("Toy", back_populates="allocations")
    subscription = relationship("Subscription")

# UserCategory Table
class UserCategory(Base):
    __tablename__ = "user_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category = Column(String, nullable=False)
    
    user = relationship("User", back_populates="categories")