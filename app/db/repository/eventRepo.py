from sqlalchemy.orm import Session
from app.db.schema.venue import EventCreate
from app.db.models import Event  # Assuming Event is the SQLAlchemy model

class EventRepository:
    @staticmethod
    def get_events_by_date(db: Session, date: str):
        return db.query(Event).filter(Event.date == date).all()

    @staticmethod
    def get_events_by_venue(db: Session, venue_id: int):
        return db.query(Event).filter(Event.venue_id == venue_id).all()

    @staticmethod
    def get_event_details(db: Session, event_id: int):
        return db.query(Event).filter(Event.id == event_id).first()

    @staticmethod
    def get_free_events(db: Session):
        return db.query(Event).filter(Event.price == 0).all()

    @staticmethod
    def get_events_after_time(db: Session, time: str):
        return db.query(Event).filter(Event.time > time).all()
