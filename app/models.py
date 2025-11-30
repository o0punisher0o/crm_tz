from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Operator(Base):
    __tablename__ = "operators"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    load_limit = Column(Integer, default=5)

    contacts = relationship("Contact", back_populates="operator")


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True)
    external_id = Column(String, unique=True, index=True)

    contacts = relationship("Contact", back_populates="lead")


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    operator_weights = relationship("SourceOperatorWeight", back_populates="source")


class SourceOperatorWeight(Base):
    __tablename__ = "source_operator_weights"

    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey("sources.id"))
    operator_id = Column(Integer, ForeignKey("operators.id"))
    weight = Column(Integer)

    source = relationship("Source", back_populates="operator_weights")
    operator = relationship("Operator")


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer, ForeignKey("leads.id"))
    source_id = Column(Integer, ForeignKey("sources.id"))
    operator_id = Column(Integer, ForeignKey("operators.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    lead = relationship("Lead", back_populates="contacts")
    operator = relationship("Operator", back_populates="contacts")
