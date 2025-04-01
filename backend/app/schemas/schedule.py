from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

from app.models.schedule import ScheduleStatus
from app.schemas.vessel import VesselNested
from app.schemas.dock import DockNested
from app.schemas.cargo import CargoNested


# Shared properties
class ScheduleBase(BaseModel):
    reference_number: Optional[str] = None
    scheduled_arrival: Optional[datetime] = None
    scheduled_departure: Optional[datetime] = None
    actual_arrival: Optional[datetime] = None
    actual_departure: Optional[datetime] = None
    status: Optional[ScheduleStatus] = ScheduleStatus.PLANNED
    notes: Optional[str] = None


# Properties to receive via API on creation
class ScheduleCreate(ScheduleBase):
    reference_number: str
    scheduled_arrival: datetime
    scheduled_departure: datetime
    vessel_id: int
    dock_id: int


# Properties to receive via API on update
class ScheduleUpdate(ScheduleBase):
    pass


# Properties to return via API
class ScheduleInDBBase(ScheduleBase):
    id: int
    vessel_id: int
    dock_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Additional properties to return via API
class Schedule(ScheduleInDBBase):
    pass


# Detailed schedule with all relationships
class ScheduleDetail(ScheduleInDBBase):
    vessel: Optional[VesselNested]
    dock: Optional[DockNested]
    cargo_shipments: Optional[List[CargoNested]] = []


# Nested schedule (used in responses that include schedule data)
class ScheduleNested(BaseModel):
    id: int
    reference_number: str
    scheduled_arrival: datetime
    scheduled_departure: datetime
    status: ScheduleStatus
    
    class Config:
        orm_mode = True