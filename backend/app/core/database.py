from sqlmodel import SQLModel, create_engine, Session
from .config import settings

engine = create_engine(
    settings.database_url,
    echo=False,
    pool_size=10,
    max_overflow=20, 
    pool_pre_ping=True
)

def get_session():
    with Session(engine) as session:
        yield session