from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Operator
from app.schemas import OperatorCreate, OperatorUpdate


router = APIRouter(prefix="/operators", tags=["Operators"])


@router.post("/")
def create_operator(data: OperatorCreate, db: Session = Depends(get_db)):
    op = Operator(name=data.name, active=data.active, load_limit=data.load_limit)
    db.add(op)
    db.commit()
    db.refresh(op)
    return op


@router.get("/")
def list_operators(db: Session = Depends(get_db)):
    return db.query(Operator).all()


@router.patch("/{operator_id}")
def update_operator(operator_id: int, data: OperatorUpdate, db: Session = Depends(get_db)):
    op = db.query(Operator).filter_by(id=operator_id).first()
    if not op:
        return {"error": "Not found"}

    if data.name is not None:
        op.name = data.name
    if data.active is not None:
        op.active = data.active
    if data.load_limit is not None:
        op.load_limit = data.load_limit

    db.commit()
    return op
