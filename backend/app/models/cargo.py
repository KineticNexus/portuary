from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from app.db.base_class import Base


class CargoType(str, enum.Enum):
    CONTAINER = "container"
    LIQUID_BULK = "liquid_bulk"
    DRY_BULK = "dry_bulk"
    BREAK_BULK = "break_bulk"
    REFRIGERATED = "refrigerated"
    VEHICLES = "vehicles"
    SPECIAL = "special"


class CargoStatus(str, enum.Enum):
    PLANNED = "planned"
    IN_TRANSIT = "in_transit"
    AT_PORT = "at_port"
    UNLOADED = "unloaded"
    DELIVERED = "delivered"
    DELAYED = "delayed"
    CANCELLED = "cancelled"


class Cargo(Base):
    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String, unique=True, index=True)
    cargo_type = Column(Enum(CargoType), index=True)
    description = Column(Text)
    weight = Column(Float)  # in metric tons
    volume = Column(Float)  # in cubic meters
    value = Column(Float)   # in currency
    status = Column(Enum(CargoStatus), default=CargoStatus.PLANNED)
    origin = Column(String)
    destination = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    owner_id = Column(Integer, ForeignKey("user.id"))
    vessel_id = Column(Integer, ForeignKey("vessel.id"))
    schedule_id = Column(Integer, ForeignKey("schedule.id"))
    
    # Relationships
    owner = relationship("User", back_populates="cargo_shipments")
    vessel = relationship("Vessel", back_populates="cargo_shipments")
    schedule = relationship("Schedule", back_populates="cargo_shipments")