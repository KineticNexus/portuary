from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from app.db.base_class import Base


class ScheduleStatus(str, enum.Enum):
    PLANNED = "planned"
    CONFIRMED = "confirmed"
    DEPARTED = "departed"
    ARRIVED = "arrived"
    COMPLETED = "completed"
    DELAYED = "delayed"
    CANCELLED = "cancelled"


class Schedule(Base):
    id = Column(Integer, primary_key=True, index=True)
    reference_number = Column(String, unique=True, index=True)
    scheduled_arrival = Column(DateTime, index=True)
    scheduled_departure = Column(DateTime, index=True)
    actual_arrival = Column(DateTime, nullable=True)
    actual_departure = Column(DateTime, nullable=True)
    status = Column(Enum(ScheduleStatus), default=ScheduleStatus.PLANNED)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    vessel_id = Column(Integer, ForeignKey("vessel.id"))
    dock_id = Column(Integer, ForeignKey("dock.id"))
    
    # Relationships
    vessel = relationship("Vessel", back_populates="schedules")
    dock = relationship("Dock", back_populates="schedules")
    cargo_shipments = relationship("Cargo", back_populates="schedule")