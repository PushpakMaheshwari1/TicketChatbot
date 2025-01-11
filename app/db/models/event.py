from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Time
from sqlalchemy.orm import relationship
from app.core.database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    name = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    time = Column(Time, nullable=False)  # Use Time type
    total_seats = Column(Integer, nullable=False)
    available_seats = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    payment_method = Column(String, nullable=False) 

    # Define the relationship to Venue
    venue = relationship("Venue", back_populates="events")
