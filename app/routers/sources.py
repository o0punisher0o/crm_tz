from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Source, SourceOperatorWeight, Operator
from app.schemas import SourceCreate, SourceWeightCreate


router = APIRouter(prefix="/sources", tags=["Sources"])


@router.post("/")
def create_source(data: SourceCreate, db: Session = Depends(get_db)):
    s = Source(name=data.name)
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


@router.get("/")
def list_sources(db: Session = Depends(get_db)):
    return db.query(Source).all()


@router.post("/{source_id}/weights")
def set_weights(source_id: int, weights: list[SourceWeightCreate], db: Session = Depends(get_db)):
    db.query(SourceOperatorWeight).filter_by(source_id=source_id).delete()

    for w in weights:
        row = SourceOperatorWeight(
            source_id=source_id,
            operator_id=w.operator_id,
            weight=w.weight
        )
        db.add(row)

    db.commit()
    return {"status": "ok"}
