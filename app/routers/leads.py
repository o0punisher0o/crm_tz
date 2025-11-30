from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Lead


router = APIRouter(prefix="/leads", tags=["Leads"])


@router.get("/")
def list_leads(db: Session = Depends(get_db)):
    return db.query(Lead).all()


@router.get("/{lead_id}")
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter_by(id=lead_id).first()
    if not lead:
        return {"error": "Not found"}
    return lead
