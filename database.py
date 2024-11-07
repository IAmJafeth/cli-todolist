from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///tasks.db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)