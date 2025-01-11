from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class EventCreate(BaseModel):
    name: str
    date: datetime
    time: str
    total_seats: int
    available_seats: int
    price: float
    payment_method: str

    class Config:
        from_attributes = True  # Allow from_orm usage


class VenueCreate(BaseModel):
    name: str
    location: str
    description: Optional[str] = None
    events: Optional[List[EventCreate]] = None

    class Config:
        from_attributes = True  # Allow from_orm usage


class VenueOut(VenueCreate):
    id: int
    events: List[EventCreate]

    class Config:
        orm_mode = True
        from_attributes = True  # Allow from_orm usage
