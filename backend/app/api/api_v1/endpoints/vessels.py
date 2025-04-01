from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.models.vessel import Vessel
from app.schemas.vessel import VesselCreate, VesselUpdate, Vessel as VesselSchema
from app.api.deps import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[VesselSchema])
def read_vessels(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve vessels.
    """
    vessels = db.query(Vessel).offset(skip).limit(limit).all()
    return vessels


@router.post("/", response_model=VesselSchema)
def create_vessel(
    *,
    db: Session = Depends(deps.get_db),
    vessel_in: VesselCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new vessel.
    """
    vessel = Vessel(**vessel_in.model_dump())
    db.add(vessel)
    db.commit()
    db.refresh(vessel)
    return vessel


@router.get("/{vessel_id}", response_model=VesselSchema)
def read_vessel(
    *,
    db: Session = Depends(deps.get_db),
    vessel_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get vessel by ID.
    """
    vessel = db.query(Vessel).filter(Vessel.id == vessel_id).first()
    if not vessel:
        raise HTTPException(status_code=404, detail="Vessel not found")
    return vessel


@router.put("/{vessel_id}", response_model=VesselSchema)
def update_vessel(
    *,
    db: Session = Depends(deps.get_db),
    vessel_id: int,
    vessel_in: VesselUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a vessel.
    """
    vessel = db.query(Vessel).filter(Vessel.id == vessel_id).first()
    if not vessel:
        raise HTTPException(status_code=404, detail="Vessel not found")
    
    update_data = vessel_in.model_dump(exclude_unset=True)
    for field in update_data:
        setattr(vessel, field, update_data[field])
        
    db.add(vessel)
    db.commit()
    db.refresh(vessel)
    return vessel


@router.delete("/{vessel_id}", response_model=VesselSchema)
def delete_vessel(
    *,
    db: Session = Depends(deps.get_db),
    vessel_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete a vessel.
    """
    vessel = db.query(Vessel).filter(Vessel.id == vessel_id).first()
    if not vessel:
        raise HTTPException(status_code=404, detail="Vessel not found")
    
    db.delete(vessel)
    db.commit()
    return vessel