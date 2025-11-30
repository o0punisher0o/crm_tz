from sqlalchemy.orm import Session
from app.models import Operator


def get_operator(db: Session, operator_id: int):
    return db.query(Operator).filter_by(id=operator_id).first()
