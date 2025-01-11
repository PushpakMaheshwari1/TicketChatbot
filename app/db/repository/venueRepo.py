from sqlalchemy.orm import Session
from app.db.models.venue import Venue
from app.db.models.event import Event
from app.db.schema.venue import VenueCreate, EventCreate

class VenueRepository:
    @staticmethod
    def create_venue(db: Session, venue_data: VenueCreate) -> Venue:
        venue = Venue(
            name=venue_data.name,
            location=venue_data.location,
            description=venue_data.description,
        )

        if venue_data.events:
            for event_data in venue_data.events:
                event = Event(
                    name=event_data.name,
                    date=event_data.date,
                    time=event_data.time,
                    total_seats=event_data.total_seats,
                    available_seats=event_data.available_seats,
                    price=event_data.price,
                    payment_method=event_data.payment_method,
                )
                venue.events.append(event)  
                
        db.add(venue)
        db.commit()
        db.refresh(venue)
        return venue


    @staticmethod
    def create_event(db: Session, event_data: EventCreate, venue_id: int):
        event = Event(**event_data.dict(), venue_id=venue_id)
        db.add(event)
        db.commit()
        db.refresh(event)
        return event

    @staticmethod
    def get_all_venues(db: Session):
        return db.query(Venue).all()

    @staticmethod
    def get_events_by_venue(db: Session, venue_id: int):
        return db.query(Event).filter(Event.venue_id == venue_id).all()
