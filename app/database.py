import os

from sqlalchemy import create_engine , event
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./rotaradar.db"
)

engine_options = {}

if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine_options["connect_args"] = {
        "check_same_thread": False
    }

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    **engine_options
)

if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):

    @event.listens_for(engine, "connect")
    def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()