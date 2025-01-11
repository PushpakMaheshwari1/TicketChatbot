# app/db/models/__init__.py
from app.db.models.venue import Venue
from app.db.models.event import Event

# This ensures that both Venue and Event are registered with the Base metadata
__all__ = ["Venue", "Event"]
