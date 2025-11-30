from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.database import get_db
from app.models import Operator
from app.schemas import OperatorCreate, OperatorUpdate, OperatorOut


router = APIRouter(
    prefix="/operators",
    tags=["Operators"]
)


@router.post("/",
             response_model=OperatorOut,
             status_code=status.HTTP_201_CREATED,
             summary="Create Operator")
def create_operator(data: OperatorCreate, db: Session = Depends(get_db)):
    op = Operator(name=data.name, active=data.active, load_limit=data.load_limit)
    db.add(op)
    db.commit()
    db.refresh(op)
    return op


@router.get("/",
            response_model=list[OperatorOut],
            summary="List Operators")
def list_operators(db: Session = Depends(get_db)):
    return db.query(Operator).all()


@router.patch("/{operator_id}",
              response_model=OperatorOut,
              summary="Update Operator")
def update_operator(operator_id: int,
                    data: OperatorUpdate,
                    db: Session = Depends(get_db)):
    op = (db.query(Operator)
          .filter_by(id=operator_id)
          .first())
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
