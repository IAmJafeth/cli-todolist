from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///tasks.db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

def get_session() -> Session:
    """
    Generates the local session bind to the DB engine.

    Returns:
        Session: Session object to interact with the DB.
    """    
    return SessionLocal()