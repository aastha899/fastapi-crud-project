from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Audit Platform Backend")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Audit Platform Backend is running ✅"}

@app.post("/audits", response_model=schemas.AuditOut)
def create_audit(audit: schemas.AuditCreate, db: Session = Depends(get_db)):
    record = models.AuditRecord(**audit.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@app.get("/audits", response_model=list[schemas.AuditOut])
def list_audits(db: Session = Depends(get_db)):
    return db.query(models.AuditRecord).order_by(models.AuditRecord.id.desc()).all()

@app.get("/audits/{audit_id}", response_model=schemas.AuditOut)
def get_audit(audit_id: int, db: Session = Depends(get_db)):
    record = db.query(models.AuditRecord).filter(models.AuditRecord.id == audit_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Audit record not found")
    return record

@app.put("/audits/{audit_id}", response_model=schemas.AuditOut)
def update_audit(audit_id: int, payload: schemas.AuditUpdate, db: Session = Depends(get_db)):
    record = db.query(models.AuditRecord).filter(models.AuditRecord.id == audit_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Audit record not found")

    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)
    return record

@app.delete("/audits/{audit_id}")
def delete_audit(audit_id: int, db: Session = Depends(get_db)):
    record = db.query(models.AuditRecord).filter(models.AuditRecord.id == audit_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Audit record not found")

    db.delete(record)
    db.commit()
    return {"message": f"Deleted audit record {audit_id} ✅"}