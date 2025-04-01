from typing import Optional, List, Dict, Any
from pydantic import BaseModel, validator
import json

from app.models.dock import DockType


# Shared properties
class DockBase(BaseModel):
    name: Optional[str] = None
    dock_number: Optional[str] = None
    dock_type: Optional[DockType] = None
    length: Optional[float] = None
    depth: Optional[float] = None
    max_draft: Optional[float] = None
    is_active: Optional[bool] = True
    location: Optional[str] = None
    coordinates: Optional[str] = None
    facilities: Optional[str] = None
    
    @validator('facilities', pre=True)
    def validate_facilities(cls, v):
        if isinstance(v, dict):
            return json.dumps(v)
        return v
    
    def get_facilities_dict(self) -> Dict[str, Any]:
        if self.facilities:
            try:
                return json.loads(self.facilities)
            except json.JSONDecodeError:
                return {}
        return {}


# Properties to receive via API on creation
class DockCreate(DockBase):
    name: str
    dock_number: str
    dock_type: DockType
    facilities: Optional[Dict[str, Any]] = None
    
    @validator('facilities', pre=True)
    def validate_facilities_dict(cls, v):
        if isinstance(v, dict):
            return json.dumps(v)
        return v


# Properties to receive via API on update
class DockUpdate(DockBase):
    facilities: Optional[Dict[str, Any]] = None
    
    @validator('facilities', pre=True)
    def validate_facilities_dict(cls, v):
        if isinstance(v, dict):
            return json.dumps(v)
        return v


# Properties to return via API
class DockInDBBase(DockBase):
    id: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class Dock(DockInDBBase):
    facilities_dict: Dict[str, Any] = None
    
    @validator('facilities_dict', always=True)
    def set_facilities_dict(cls, v, values):
        if 'facilities' in values and values['facilities']:
            try:
                return json.loads(values['facilities'])
            except json.JSONDecodeError:
                return {}
        return {}


# Nested dock (used in responses that include dock data)
class DockNested(BaseModel):
    id: int
    name: str
    dock_number: str
    dock_type: DockType
    
    class Config:
        orm_mode = True