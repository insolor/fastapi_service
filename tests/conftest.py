import os
import tempfile

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from starlette.testclient import TestClient

from inside.app import app
from inside.database import Base, get_db


@pytest.fixture(scope="session")
def db_fixture() -> Session:
    _, db_file = tempfile.mkstemp(suffix=".db")
    engine = create_engine(
        "sqlite:///" + db_file, connect_args=dict(check_same_thread=False)
    )
    Base.metadata.create_all(bind=engine)
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = session_local()
    try:
        yield db
    finally:
        db.close()
        os.remove(db_file)


@pytest.fixture(scope="session")
def client(db_fixture) -> TestClient:
    def _get_db_override():
        return db_fixture

    app.dependency_overrides[get_db] = _get_db_override
    return TestClient(app)


@pytest.fixture(scope="session")
def token(client) -> str:
    return client.post(
        "/user/signup",
        json=dict(name="user1", password="123"),
    ).json()["token"]
