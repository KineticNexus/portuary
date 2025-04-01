from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.models.dock import Dock
from app.schemas.dock import DockCreate, DockUpdate, Dock as DockSchema
from app.api.deps import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[DockSchema])
def read_docks(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve docks.
    """
    docks = db.query(Dock).offset(skip).limit(limit).all()
    return docks


@router.post("/", response_model=DockSchema)
def create_dock(
    *,
    db: Session = Depends(deps.get_db),
    dock_in: DockCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new dock.
    """
    dock = Dock(**dock_in.model_dump())
    db.add(dock)
    db.commit()
    db.refresh(dock)
    return dock


@router.get("/{dock_id}", response_model=DockSchema)
def read_dock(
    *,
    db: Session = Depends(deps.get_db),
    dock_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get dock by ID.
    """
    dock = db.query(Dock).filter(Dock.id == dock_id).first()
    if not dock:
        raise HTTPException(status_code=404, detail="Dock not found")
    return dock


@router.put("/{dock_id}", response_model=DockSchema)
def update_dock(
    *,
    db: Session = Depends(deps.get_db),
    dock_id: int,
    dock_in: DockUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a dock.
    """
    dock = db.query(Dock).filter(Dock.id == dock_id).first()
    if not dock:
        raise HTTPException(status_code=404, detail="Dock not found")
    
    update_data = dock_in.model_dump(exclude_unset=True)
    for field in update_data:
        setattr(dock, field, update_data[field])
        
    db.add(dock)
    db.commit()
    db.refresh(dock)
    return dock


@router.delete("/{dock_id}", response_model=DockSchema)
def delete_dock(
    *,
    db: Session = Depends(deps.get_db),
    dock_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete a dock.
    """
    dock = db.query(Dock).filter(Dock.id == dock_id).first()
    if not dock:
        raise HTTPException(status_code=404, detail="Dock not found")
    
    db.delete(dock)
    db.commit()
    return dock