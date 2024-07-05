import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..main import app
from ..databases.db import Base, get_auth_db
from .auth import models as auth_models

test_engine = create_engine(url="sqlite:///./pytest.db", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    # Create the tables
    Base.metadata.create_all(bind=test_engine)

    # Yield so that tests can run
    yield

    # After all tests have run, drop all tables
    Base.metadata.drop_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:        
        yield db
    finally:
        db.close()

# override the get_db dependency with test session
app.dependency_overrides[get_auth_db] = override_get_db


client = TestClient(app)


def test_create_roles_and_groups():
    response = client.get("/init_db")
    db = next(override_get_db())

    assert response.status_code == 200

def test_create_user():

    #group_list = db.query(auth_models.Group).filter(auth_models.Group.name=="HEARTS").first()

    response = client.post(
        "/auth/register",
        json={
            "username": "test1@mail.com",
            "name": "Test1",
            "password": "test",
            "is_active": True,
            "disabled": False,
            "groups": [],
            "additional_scopes": "",
            "role": "guest",
            "password_confirm": "test"
            }
    )
    assert response.status_code == 200

    response2 = client.post(
        "/auth/register",
        json={
            "username": "test2@mail.com",
            "name": "Test2",
            "password": "test",
            "is_active": True,
            "disabled": False,
            "groups": [
                "hearts",
                "clubs"
            ],
            "additional_scopes": "test:write test:read",
            "role": "user",
            "password_confirm": "test"
            }
    )
    assert response2.status_code == 200

    db = next(override_get_db())

    assert db.query(db.query(auth_models.User).filter(auth_models.User.username == "test1@mail.com").exists()).scalar() == True
    assert db.query(db.query(auth_models.User).filter(auth_models.User.username == "test2@mail.com").exists()).scalar() == True

    assert db.query(auth_models.User).filter(auth_models.User.username == "test2@mail.com").first().groups[0].name in ["HEARTS", "CLUBS"]



## TODO: add more tests for the other endpoints