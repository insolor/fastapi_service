import functools

from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from inside.db_models import Base


@functools.lru_cache()
def get_engine():
    database_url = config("DATABASE_URL")

    connect_args = (
        dict(check_same_thread=False) if database_url.startswith("sqlite:") else dict()
    )

    engine = create_engine(database_url, connect_args=connect_args)
    Base.metadata.create_all(bind=engine)
    return engine


@functools.lru_cache()
def get_session_factory():
    return sessionmaker(autocommit=False, autoflush=False, bind=get_engine())


def get_session():
    session_local = get_session_factory()
    db = session_local()
    try:
        yield db
    finally:
        db.close()
