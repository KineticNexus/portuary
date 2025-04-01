from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from app.db.base_class import Base


class VesselType(str, enum.Enum):
    CONTAINER = "container"
    BULK_CARRIER = "bulk_carrier"
    TANKER = "tanker"
    FISHING = "fishing"
    PASSENGER = "passenger"
    TUGBOAT = "tugboat"
    OTHER = "other"


class Vessel(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    imo_number = Column(String, unique=True, index=True)
    vessel_type = Column(Enum(VesselType), index=True)
    length = Column(Float)
    width = Column(Float)
    draft = Column(Float)
    capacity = Column(Float)  # in metric tons
    
    # Foreign keys
    owner_id = Column(Integer, ForeignKey("user.id"))
    
    # Relationships
    owner = relationship("User", back_populates="vessels")
    schedules = relationship("Schedule", back_populates="vessel")
    cargo_shipments = relationship("Cargo", back_populates="vessel")