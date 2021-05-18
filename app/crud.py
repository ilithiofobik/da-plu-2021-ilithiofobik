from fastapi import HTTPException, status
from sqlalchemy import func, update
from sqlalchemy.orm import Session
import models
import schemas


# 5.1
def get_suppliers(db: Session):
    return (
        db.query(models.Supplier).order_by(models.Supplier.SupplierID.asc()).all()
    )


def get_suppliers_id(db: Session, id: int):
    return (
        db.query(models.Supplier).filter(models.Supplier.SupplierID == id).first()
    )


# 5.2
def get_suppliers_id_products(db: Session, id: int):
    return (
        db.query(models.Product).filter(models.Product.SupplierID == id).order_by(models.Product.ProductID.desc()).all()
    )


# 5.3
def post_suppliers(db: Session, new_supplier: schemas.PostSupplier):
    new_supplier.SupplierID = db.query(func.max(models.Supplier.SupplierID)).scalar() + 1
    db.add(models.Supplier(**new_supplier.dict()))
    db.commit()
    return get_suppliers_id(db, new_supplier.SupplierID)


# 5.4
def put_suppliers_id(db: Session, id: int, supplier_update: schemas.PutSupplier):
    properties_to_update = {key: value for key, value in supplier_update.dict().items() if value is not None}
    update_statement = update(models.Supplier).where(models.Supplier.SupplierID == id).values(**properties_to_update)
    db.execute(update_statement)
    db.commit()
    return get_suppliers_id(db, id)


# 5.5
def delete_suppliers_id(db: Session, id: int):
    check_supplier = get_suppliers_id(db, id)
    if not check_supplier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.query(models.Supplier).filter(models.Supplier.SupplierID == id).delete()
    db.commit()
