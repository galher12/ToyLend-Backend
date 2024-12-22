from typing import List
from pydantic import BaseModel

# ... existing schemas ...

class SubscriptionResponse(BaseModel):
    message: str
    toys: List[str]
