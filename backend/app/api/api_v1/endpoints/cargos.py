from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.models.cargo import Cargo
from app.schemas.cargo import CargoCreate, CargoUpdate, Cargo as CargoSchema
from app.api.deps import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[CargoSchema])
def read_cargos(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve cargos.
    """
    cargos = db.query(Cargo).offset(skip).limit(limit).all()
    return cargos


@router.post("/", response_model=CargoSchema)
def create_cargo(
    *,
    db: Session = Depends(deps.get_db),
    cargo_in: CargoCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new cargo.
    """
    cargo = Cargo(**cargo_in.model_dump())
    db.add(cargo)
    db.commit()
    db.refresh(cargo)
    return cargo


@router.get("/{cargo_id}", response_model=CargoSchema)
def read_cargo(
    *,
    db: Session = Depends(deps.get_db),
    cargo_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get cargo by ID.
    """
    cargo = db.query(Cargo).filter(Cargo.id == cargo_id).first()
    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo not found")
    return cargo


@router.put("/{cargo_id}", response_model=CargoSchema)
def update_cargo(
    *,
    db: Session = Depends(deps.get_db),
    cargo_id: int,
    cargo_in: CargoUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a cargo.
    """
    cargo = db.query(Cargo).filter(Cargo.id == cargo_id).first()
    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo not found")
    
    update_data = cargo_in.model_dump(exclude_unset=True)
    for field in update_data:
        setattr(cargo, field, update_data[field])
        
    db.add(cargo)
    db.commit()
    db.refresh(cargo)
    return cargo


@router.delete("/{cargo_id}", response_model=CargoSchema)
def delete_cargo(
    *,
    db: Session = Depends(deps.get_db),
    cargo_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete a cargo.
    """
    cargo = db.query(Cargo).filter(Cargo.id == cargo_id).first()
    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo not found")
    
    db.delete(cargo)
    db.commit()
    return cargo