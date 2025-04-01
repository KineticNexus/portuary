from typing import Optional, List
from pydantic import BaseModel

from app.models.vessel import VesselType


# Shared properties
class VesselBase(BaseModel):
    name: Optional[str] = None
    imo_number: Optional[str] = None
    vessel_type: Optional[VesselType] = None
    length: Optional[float] = None
    width: Optional[float] = None
    draft: Optional[float] = None
    capacity: Optional[float] = None


# Properties to receive via API on creation
class VesselCreate(VesselBase):
    name: str
    imo_number: str
    vessel_type: VesselType


# Properties to receive via API on update
class VesselUpdate(VesselBase):
    pass


# Properties to return via API
class VesselInDBBase(VesselBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class Vessel(VesselInDBBase):
    pass


# Nested vessel (used in responses that include vessel data)
class VesselNested(BaseModel):
    id: int
    name: str
    imo_number: str
    vessel_type: VesselType
    
    class Config:
        orm_mode = True