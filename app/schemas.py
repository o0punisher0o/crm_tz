from pydantic import BaseModel
from typing import Optional


class OperatorCreate(BaseModel):
    name: str
    active: bool = True
    load_limit: int = 5


class OperatorUpdate(BaseModel):
    name: Optional[str] = None
    active: Optional[bool] = None
    load_limit: Optional[int] = None


class SourceCreate(BaseModel):
    name: str


class SourceWeightCreate(BaseModel):
    operator_id: int
    weight: int


class LeadCreate(BaseModel):
    external_id: str


class ContactCreate(BaseModel):
    external_id: str
    source_id: int
