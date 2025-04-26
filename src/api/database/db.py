"method for getting a session, to query the db."

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()
USER = os.environ.get("POSTGRES_USER", "test")
PW = os.environ.get("POSTGRES_PASSWORD", "pwd")

DB = os.environ.get("POSTGRES_DB", "db")
PORT = os.environ.get("POSTGRES_PORT", "5432")

CONN_STR = f"postgresql://{USER}:{PW}@postgres:{PORT}/{DB}"
engine = create_engine(CONN_STR)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_db():
    """
    get a database session.
    """
    db = SessionLocal()
    try:
        return db
    except Exception as e:
        db.close()
        raise e
