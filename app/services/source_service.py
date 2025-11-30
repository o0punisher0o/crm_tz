from sqlalchemy.orm import Session
from app.models import Source


def get_source(db: Session, source_id: int):
    return db.query(Source).filter_by(id=source_id).first()
