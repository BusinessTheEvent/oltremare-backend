import platform
from typing import Annotated
from fastapi import Depends, FastAPI, Response, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy import inspect, text
from src.auth.models import Role, User
from src.config import settings
from src.auth.models import User
import os
from src.databases.db import create_all, engine_internal, get_db, init_roles_table, init_users_table, init_tables_with_file
from src.default_logger import get_custom_logger
from src.auth.router import router as auth_router
from src.v01.router import router as v01_router
from sqlalchemy.orm import Session
from src.auth.middlewares import AuthCookieMiddleware

logger = get_custom_logger(__name__)


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_DEFAULT_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(version="1.0.3", title="FastAPI authentication core", description="This template provides a robust starting point for implementing authorization in your application. It includes features such as role-based access control, token-based authentication, and user management. The template is designed to be flexible and easy to integrate into existing projects, with clear documentation and modular code. Whether you're building a small application or a large, complex system, this authorization template can help you ensure that your resources are protected and only accessible to authorized users.")

if settings.USE_COOKIES_AUTH:
    app.add_middleware(AuthCookieMiddleware)

print("Using cookies for authentication: ", settings.USE_COOKIES_AUTH)

app.include_router(auth_router, prefix="/auth")
app.include_router(v01_router, prefix="/v01", tags=["v01"])


@app.get("/")
def index():
    return Response(status_code=status.HTTP_200_OK)


# Auth database startup
# case 1: no database exists
# case 2: database exists, but no tables
# case 3: database exists, and tables exist
# case 4: database exists, tables exist, but no roles or groups
# case 5: database exists, tables exist, roles and groups exist, but no admin user
# case 6: database exists but must be reinitialized so then -> case 1

def db_start():
    """
    Start the database initialization process.

    This function checks if the database exists and creates it if it doesn't.
    It also checks for tables in the database and creates them if they don't exist.
    Finally, it inspects the tables and checks for empty tables, filling them with default data if necessary.
    """

    if not settings.AUTH_DATABASE_CHECK:
        logger.info("Database check is disabled. Skipping database initialization.")
        return

    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_url = str(engine_internal.url)
    db_path = db_url.split("///")[-1].replace("./", "")
    db_path = os.path.join(current_dir, db_path)
    
    ## TODO: adapt for postgresql
    
    if os.path.exists(db_path):
        logger.info("Database exists.")
        
        if settings.AUTH_DATABASE_PURGE:
            logger.info("Purging database as environments tell.")
            yn = input("Are you sure you want to delete the database? (y/n): ")
            if yn.lower() == "y":
                os.remove(db_path)
                logger.info("Database purged.")
                create_all()
                logger.info("Database created.")

        else:
            logger.info("No need to purge database, checking for tables.")

    elif not os.path.exists(db_path):
        logger.info("Database does not exist")
        logger.info("Creating database.")
        create_all()

    inspector = inspect(engine_internal)
    tables = inspector.get_table_names()
    if len(tables) == 0:
        logger.info("No tables found.")
        logger.info("Creating tables.")
        create_all()

    elif len(tables) > 0:
        logger.info("Tables found.")

        if settings.DEBUG:
            for table in tables:
                logger.debug(f"Inspecting table: <{table}>")
                columns = inspector.get_columns(table)

                for column in columns:
                    logger.debug(f"Column: {column['name']}, Type: {column['type']}")

                logger.debug(f"End of table <{table}> inspection.")

        with Session(engine_internal) as session:

            empty_tables = []

            for table in tables:
                if settings.DEBUG:
                    logger.debug(f"Inspecting table: <{table}>")

                # Count the number of rows in the table
                count = session.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
                if count == 0:
                    if settings.DEBUG:
                        logger.debug(f"Table <{table}> is empty.")
                    empty_tables.append(table)
                else:
                    if settings.DEBUG:
                        logger.debug(f"Table <{table}> is not empty.")
            if settings.AUTH_DATABASE_INIT_TABLES:
                logger.info(f"Filling empty tables ({empty_tables}) with default data from configuration.")

                for table in empty_tables:
                    if table == "roles":
                        init_roles_table(Role)
                    elif table == "users":
                        init_users_table(User, Role, pwd_context)
                    else:
                        logger.info(f"Table <{table}> does not need to be initialized.")
            else:
                logger.info("Tables will not be initialized as environments tell.")

    logger.info("Database initialization complete.")

db_start()
init_tables_with_file("src/databases/db_init.sql", db= Annotated[Session, Depends(get_db)])

@app.get("/info")
def get_hardware_info():
    # Get system information
    system_info = {
        "system": platform.system(),
        "node": platform.node(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
    }

    return system_info