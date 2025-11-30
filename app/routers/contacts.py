from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Contact
from app.schemas import ContactCreate
from app.services.lead_service import get_or_create_lead
from app.services.assignment_service import get_available_operators, choose_operator


router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.post("/")
def create_contact(data: ContactCreate, db: Session = Depends(get_db)):
    lead = get_or_create_lead(db, data.external_id)

    available = get_available_operators(db, data.source_id)
    operator = choose_operator(available)

    contact = Contact(
        lead_id=lead.id,
        source_id=data.source_id,
        operator_id=operator.id if operator else None
    )

    db.add(contact)
    db.commit()
    db.refresh(contact)

    return {
        "contact_id": contact.id,
        "lead_id": lead.id,
        "source_id": data.source_id,
        "assigned_operator": operator.id if operator else None
    }


@router.get("/")
def list_contacts(db: Session = Depends(get_db)):
    return db.query(Contact).all()
