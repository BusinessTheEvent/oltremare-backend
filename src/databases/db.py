import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from ..default_logger import get_custom_logger
from ..config import settings
import os

logger = get_custom_logger(__name__)

if not os.environ.get("TESTING"):
    logger.info(f"Creating connection to: {settings.SQLALCHEMY_AUTH_DATABASE_URL}.")
    engine_internal_auth = create_engine(settings.SQLALCHEMY_AUTH_DATABASE_URL, connect_args={"check_same_thread": False}) # check_same_thread = False only for sqlite
else: 
    logger.info(f"Creating connection to: dummy internal.")
    engine_internal_auth= create_engine("sqlite:///./auth_test.db", connect_args={"check_same_thread": False})


InternalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine_internal_auth)


Base = declarative_base()


def get_auth_db():
    db = InternalSession()
    try:
        yield db
    finally:
        db.close()

def create_all():
    Base.metadata.create_all(bind=engine_internal_auth)

def init_users_table(model):
    pass

def init_roles_table(role_model):
    ## TODO: find a way to import data from configs
    roles = [
        {
            "name": "GUEST",
            "scopes": ""
        },
        {
            "name": "USER",
            "scopes": "dashboard:read settings:read docs:read profile:read"
        },
        {
            "name": "STAFF",
            "scopes": "dashboard:read settings:read settings:write docs:read docs:write profile:read"
        },
        {
            "name": "ADMIN",
            "scopes": "dashboard:read settings:read settings:write docs:read docs:write docs:delete profile:read profile:write users:read users:write users:delete roles:read roles:write roles:delete"
        }
    ]
    
    with Session(engine_internal_auth) as db:
        for role in roles:
            db_role = role_model(**role)
            db.add(db_role)
            if settings.DEBUG:
                logger.debug(f"Role {db_role.name} created")
        db.commit()

def init_users_table(user_model, role_model, pwd_context):
    ## TODO: find a way to import data from configs
    with Session(engine_internal_auth) as db:
        new_user = user_model(
            username="admin",
            name="Administrator",
            password=pwd_context.hash("admin"),
            is_active=True,
            disabled=False,
            scopes="",
            registered_at=datetime.datetime.utcnow()
        )
        new_user.role=db.query(role_model).filter(role_model.name == "ADMIN").first()
        db.add(new_user)
        db.commit()

        if settings.DEBUG:
            logger.debug(f"User {new_user.username} created")