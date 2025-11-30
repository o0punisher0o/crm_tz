from fastapi import FastAPI
from app.database import Base, engine
from app.routers import operators, sources, leads, contacts


Base.metadata.create_all(bind=engine)


app = FastAPI(title="Mini CRM")


app.include_router(operators.router)
app.include_router(sources.router)
app.include_router(leads.router)
app.include_router(contacts.router)
