from sqlalchemy.orm import Session
from app.db.repository.venueRepo import VenueRepository
from app.db.schema.venue import VenueCreate, EventCreate, VenueOut
from app.db.models.venue import Venue

class VenueService:
    @staticmethod
    def add_venue(db: Session, venue_data: VenueCreate) -> VenueOut:
        venue = VenueRepository.create_venue(db, venue_data)
        return venue

    @staticmethod
    def add_event(db: Session, venue_id: int, event_data: EventCreate):
        return VenueRepository.create_event(db, event_data, venue_id)

    @staticmethod
    def get_venues(db: Session):
        venues = VenueRepository.get_all_venues(db)
        return [VenueOut.from_orm(venue) for venue in venues]

    @staticmethod
    def get_events(db: Session, venue_id: int):
        return VenueRepository.get_events_by_venue(db, venue_id)
