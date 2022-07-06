import os
import tempfile

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from starlette.testclient import TestClient

from inside.app import app, get_db
from inside.database import Base


@pytest.fixture(scope="session")
def db_fixture() -> Session:
    _, db_file = tempfile.mkstemp(suffix=".db")
    engine = create_engine("sqlite:///" + db_file, connect_args=dict(check_same_thread=False))
    Base.metadata.create_all(bind=engine)
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    try:
        yield session_local()
    finally:
        os.remove(db_file)


@pytest.fixture(scope="session")
def client(db_fixture) -> TestClient:

    def _get_db_override():
        return db_fixture

    app.dependency_overrides[get_db] = _get_db_override
    return TestClient(app)
