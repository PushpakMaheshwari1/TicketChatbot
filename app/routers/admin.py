from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.db.schema.venue import VenueCreate, EventCreate, VenueOut
from typing import List
from app.util.protectRoute import get_current_user
from app.service.venueService import VenueService

adminRouter = APIRouter()

@adminRouter.post("/venues/", response_model=VenueOut)
def create_venue(venue_data: VenueCreate, db: Session = Depends(get_db)):
    venue = VenueService.add_venue(db, venue_data)
    if not venue:
        raise HTTPException(status_code=400, detail="Failed to create venue")
    return venue

@adminRouter.post("/venues/{venue_id}/events/", response_model=EventCreate)
def create_event(venue_id: int, event_data: EventCreate, db: Session = Depends(get_db)):
    event = VenueService.add_event(db, venue_id, event_data)
    if not event:
        raise HTTPException(status_code=400, detail="Failed to create event")
    return event

@adminRouter.get("/venues/", response_model=List[VenueOut])
def list_venues(db: Session = Depends(get_db)):
    return VenueService.get_venues(db)

@adminRouter.get("/venues/{venue_id}/events/", response_model=List[EventCreate])
def list_events(venue_id: int, db: Session = Depends(get_db)):
    events = VenueService.get_events(db, venue_id)
    if not events:
        raise HTTPException(status_code=404, detail="No events found for this venue")
    return events
