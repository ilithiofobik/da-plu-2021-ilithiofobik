from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import PositiveInt
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db

router = APIRouter()


# 5.1
@router.get("/suppliers", response_model=List[schemas.SimpleSupplier])
async def get_suppliers(db: Session = Depends(get_db)):
    return crud.get_suppliers(db)


@router.get("/suppliers/{id}", response_model=schemas.Supplier)
async def get_suppliers_id(id: PositiveInt, db: Session = Depends(get_db)):
    supplier = crud.get_suppliers_id(db, id)
    if supplier:
        return supplier
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


# 5.2
@router.get("/suppliers/{id}/products", response_model=List[schemas.Product])
async def get_suppliers_id_products(id: PositiveInt, db: Session = Depends(get_db)):
    products = crud.get_suppliers_id_products(db, id)
    if products:
        return products
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


# 5.3
@router.post("/suppliers", response_model=schemas.Supplier, status_code=status.HTTP_201_CREATED)
async def post_suppliers(supplier: schemas.PostSupplier, db: Session = Depends(get_db)):
    return crud.post_suppliers(db, supplier)


# 5.4
@router.put("/suppliers/{id}", response_model=schemas.Supplier)
async def put_suppliers_id(id: int, supplier: schemas.PutSupplier, db: Session = Depends(get_db)):
    updated = crud.put_suppliers_id(db, id, supplier)
    if updated:
        return updated
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


# 5.5
@router.delete("/suppliers/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_suppliers_id(id: int, db: Session = Depends(get_db)):
    crud.delete_suppliers_id(db, id)
