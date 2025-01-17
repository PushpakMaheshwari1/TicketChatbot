from sqlalchemy.orm import Session
from app.db.models.event import Event
from app.db.models import Venue
from datetime import datetime

class EventRepository:
    @staticmethod
    def get_all_events(db: Session):
        return db.query(Event).all()

    @staticmethod
    def find_event_by_date(date: datetime, db: Session):
        return db.query(Event).filter(Event.date == date).all()

    @staticmethod
    def find_event_by_venue(venue_name: str, db: Session):
        venue = db.query(Venue).filter(Venue.name.ilike(f"%{venue_name}%")).first()
        if venue:
            return db.query(Event).filter(Event.venue_id == venue.id).all()
        return []

    @staticmethod
    def get_event_price(event_name: str, db: Session):
        event = db.query(Event).filter(Event.name.ilike(f"%{event_name}%")).first()
        return {"price": event.price} if event else None

    @staticmethod
    def get_event_details(event_name: str, db: Session):
        event = db.query(Event).filter(Event.name.ilike(f"%{event_name}%")).first()
        if event:
            return {
                "name": event.name,
                "date": event.date,
                "time": event.time,
                "available_seats": event.available_seats,
            }
        return None

    @staticmethod
    def find_free_events(db: Session):
        return db.query(Event).filter(Event.price == 0).all()
