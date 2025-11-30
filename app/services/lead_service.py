from sqlalchemy.orm import Session
from app.models import Lead


def get_or_create_lead(db: Session, external_id: str):
    lead = db.query(Lead).filter_by(external_id=external_id).first()
    if lead:
        return lead
    lead = Lead(external_id=external_id)
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead
