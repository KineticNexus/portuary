from sqlalchemy import Column, Integer, String, Float, Boolean, Enum, Text
from sqlalchemy.orm import relationship
import enum

from app.db.base_class import Base


class DockType(str, enum.Enum):
    CONTAINER = "container"
    BULK = "bulk"
    TANKER = "tanker"
    PASSENGER = "passenger"
    MULTIPURPOSE = "multipurpose"


class Dock(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    dock_number = Column(String, unique=True, index=True)
    dock_type = Column(Enum(DockType), index=True)
    length = Column(Float)  # in meters
    depth = Column(Float)   # in meters
    max_draft = Column(Float)  # in meters
    is_active = Column(Boolean, default=True)
    location = Column(String)
    coordinates = Column(String)  # Format: "latitude,longitude"
    facilities = Column(Text)  # JSON string with available facilities
    
    # Relationships
    schedules = relationship("Schedule", back_populates="dock")