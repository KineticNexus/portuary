from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

from app.models.cargo import CargoType, CargoStatus


# Shared properties
class CargoBase(BaseModel):
    tracking_number: Optional[str] = None
    cargo_type: Optional[CargoType] = None
    description: Optional[str] = None
    weight: Optional[float] = None
    volume: Optional[float] = None
    value: Optional[float] = None
    status: Optional[CargoStatus] = CargoStatus.PLANNED
    origin: Optional[str] = None
    destination: Optional[str] = None


# Properties to receive via API on creation
class CargoCreate(CargoBase):
    tracking_number: str
    cargo_type: CargoType
    origin: str
    destination: str
    vessel_id: Optional[int] = None
    schedule_id: Optional[int] = None


# Properties to receive via API on update
class CargoUpdate(CargoBase):
    pass


# Properties to return via API
class CargoInDBBase(CargoBase):
    id: int
    owner_id: int
    vessel_id: Optional[int] = None
    schedule_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Additional properties to return via API
class Cargo(CargoInDBBase):
    pass


# Nested cargo (used in responses that include cargo data)
class CargoNested(BaseModel):
    id: int
    tracking_number: str
    cargo_type: CargoType
    status: CargoStatus
    weight: Optional[float] = None
    origin: str
    destination: str
    
    class Config:
        orm_mode = True