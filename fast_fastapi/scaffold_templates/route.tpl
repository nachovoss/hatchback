from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.__resource__ import __Resource__Create, __Resource__Update, __Resource__Response
from app.services.__resource__ import __Resource__Service

router = APIRouter(prefix="/__resource__s", tags=["__Resource__s"])

def get_service(db: Session = Depends(get_db)):
    return __Resource__Service(db)

@router.get("/", response_model=List[__Resource__Response])
def read_all(skip: int = 0, limit: int = 100, service: __Resource__Service = Depends(get_service)):
    return service.get_all(skip, limit)

@router.get("/{id}", response_model=__Resource__Response)
def read_one(id: UUID, service: __Resource__Service = Depends(get_service)):
    item = service.get(id)
    if not item:
        raise HTTPException(status_code=404, detail="__Resource__ not found")
    return item

@router.post("/", response_model=__Resource__Response)
def create(item: __Resource__Create, service: __Resource__Service = Depends(get_service)):
    return service.create(item.model_dump())

@router.put("/{id}", response_model=__Resource__Response)
def update(id: UUID, item: __Resource__Update, service: __Resource__Service = Depends(get_service)):
    return service.update(id, item.model_dump(exclude_unset=True))

@router.delete("/{id}")
def delete(id: UUID, service: __Resource__Service = Depends(get_service)):
    return service.delete(id)
