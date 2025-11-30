import random
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models import Operator, SourceOperatorWeight, Contact


def get_available_operators(db: Session, source_id: int):
    weights = db.query(SourceOperatorWeight).filter_by(source_id=source_id).all()
    result = []

    for w in weights:
        op = db.query(Operator).filter_by(id=w.operator_id).first()
        if not op or not op.active:
            continue

        # нагрузка за 24 часа
        limit = op.load_limit
        active_contacts = db.query(Contact).filter(
            Contact.operator_id == op.id,
            Contact.created_at >= datetime.utcnow() - timedelta(hours=24)
        ).count()

        if active_contacts < limit:
            result.append((op, w.weight))

    return result


def choose_operator(available):
    if not available:
        return None

    operators, weights = zip(*available)
    total = sum(weights)
    r = random.uniform(0, total)
    cur = 0

    for op, w in zip(operators, weights):
        cur += w
        if r <= cur:
            return op

    return None
