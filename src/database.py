from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from typing import Generator
from models import Base
from logger import setup_logger, get_logger

DATABASE_URL = "sqlite:///../data/tasks.db"  # Default database URL

# Logger for error handling or debug purposes
setup_logger("database")
logger = get_logger("database")

class Database:
    """Singleton-like database session manager."""

    _engine = None
    _SessionLocal = None

    @classmethod
    def setup(cls, database_url: str = DATABASE_URL) -> None:
        """Initializes the database engine and session factory."""
        if cls._engine is None:
            try:
                cls._engine = create_engine(database_url, echo=False, future=True)
                cls._SessionLocal = sessionmaker(bind=cls._engine)
                logger.info("Database engine created and session factory initialized.")
            except SQLAlchemyError as e:
                logger.error(f"Failed to initialize the database engine: {e}")
                raise

    @classmethod
    @contextmanager
    def get_session(cls) -> Generator[Session, None, None]:
        """Provides a new database session, ensuring the session factory is initialized."""
        if cls._SessionLocal is None:
            logger.debug("Session factory not initialized; setting up now.")
            cls.setup()

        session = cls._SessionLocal()
        try:
            yield session
        finally:
            session.close()

    @classmethod
    def run_migrations(cls) -> None:
        """Creates all tables in the database if they don't exist."""
        if cls._engine is None:
            cls.setup()
        logger.info("Running migrations (creating tables if not exists).")
        Base.metadata.create_all(bind=cls._engine)