import datetime
from typing import Annotated, Optional
from fastapi import Depends, HTTPException, Security, status
from passlib.context import CryptContext
from pydantic import ValidationError
from .models import User
from ..databases.db import get_db
from ..config import settings
from ..default_logger import get_custom_logger
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from ..schemas.authentication_schemas import TokenData, UserWithPassword
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

# Creating a password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = get_custom_logger(__name__)

## Defining the OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/token", ## The endpoint to get the token
    scopes={} # The scopes that the token will have
)


"""
    AUTHENTICATION FLOW DIAGRAM WHEN /token FUNCTION IS CALLED

    login() -> authenticate_user() -> get_user_from_db() -> verify_password() -> login() -> create_access_token() = TOKEN OBJECT
  
    
    AUTHENTICATION FLOW DIAGRAM WHEN get_current_active_user() DEPENDENCY IS CALLED

    get_current_active_user() ->  get_current_user() -> get_user_from_db() -> get_current_active_user() = USER OBJECT

"""


def verify_password(plain_password, hashed_password):
    """
    Verify if a plain password matches a hashed password.

    Args:
        plain_password (str): The plain password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the plain password matches the hashed password, False otherwise.
    """
    logger.debug(f"Verifying password")
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Hashes the given password using the password hashing algorithm.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.
    """
    logger.debug(f"Hashing password")
    return pwd_context.hash(password)

def get_user_from_db(db: Session, username: str):
    """
    Retrieve a user from the database based on the provided username.

    Args:
        db (Session): The database session.
        username (str): The username of the user to retrieve.

    Returns:
        UserWithPassword: The user object with additional information like hashed password and scopes.
            Returns None if the user is not found in the database.
    """
    logger.debug(f"Getting user from db")
    found_user = db.query(User).filter(User.username == username).first()

    if found_user is None:
        logger.warning(f"User {username} not found")
        return None
    else:
        ## manually passing the role and group list as it is not included in the __dict__ because it is a relationship
        return UserWithPassword(
            **found_user.__dict__,
            role=found_user.role.__dict__, 
            groups=[group.__dict__ for group in found_user.groups], 
            all_scopes=" ".join(found_user.get_all_scopes()) ## Adding all the scopes of the user manually because get_all_scopes() is a method
        )
    
def authenticate_user(db: Session, username: str, password: str):
    """
    Authenticates a user by checking the provided username and password against the database.

    Args:
        db (Session): The database session.
        username (str): The username of the user to authenticate.
        password (str): The password of the user to authenticate.

    Returns:
        Union[User, bool]: The authenticated user object if successful, False otherwise.
    """
    logger.debug(f"Authenticating user")
    user = get_user_from_db(db, username)
    if not user:
        logger.warning(f"User {username} not found")
        return False
    if not verify_password(password, user.password.get_secret_value()):
        logger.warning(f"Invalid password for user {username}")
        return False
    
    logger.debug(f"User {username} authenticated")
    return user

def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
    """
    Create an access token with the provided data.

    Args:
        data (dict): The data to be encoded in the access token.
        expires_delta (Optional[datetime.timedelta]): Optional expiration time for the access token.

    Returns:
        str: The encoded access token.

    """
    logger.debug(f"Creating access token")

    
    to_encode = data.copy() ## Copying the data to avoid modifying the original dictionary

    ## Adding the expiration time to the token
    if expires_delta:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_delta)
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Encoding the token with the app secret key
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt

async def get_current_user(security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)]) -> User:
    """
    Retrieves the current user based on the provided security scopes and token.

    Args:
        security_scopes (SecurityScopes): The security scopes associated with the request.
        token (str): The authentication token.
        db (Session): The database session.

    Returns:
        User: The current user.

    Raises:
        HTTPException: If the credentials cannot be validated or if the user does not have enough permissions.
    """
    logger.debug(f"Getting current user")

    # Checking if the token has the required scopes
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"' # Adding the scopes to the authenticate header
    else:
        authenticate_value = "Bearer" # If no scopes are passed, the authenticate header will be just "Bearer"

    # Creating the exception to be raised if the credentials are not valid
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]) ## Decoding the token
        username: str = payload.get("sub") # Getting the username from the token
        
        if username is None:
            raise credentials_exception
        
        token_scopes = payload.get("scopes", []) # Getting the scopes from the token
        token_data = TokenData(scopes=token_scopes, username=username) ## Validate data by creating a TokenData object with the scopes and username from the token
    
    except (JWTError, ValidationError):
        raise credentials_exception
    
    user = get_user_from_db(db, username=token_data.username) # Getting the user from the database
    if user is None:
        raise credentials_exception
    
    ## Checking the scopes passed to the function with the ones from the token (that should be the user.all_scopes)
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes: ## FIXME: maybe fetch scoper directly from user model to decrease amount of information sent outside the server
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
        
    return user

async def get_current_active_user(current_user: Annotated[User, Security(get_current_user, scopes=[])]):
    """
    Get the current active user.

    Args:
        current_user (User): The current user object.

    Returns:
        User: The current active user.

    Raises:
        HTTPException: If the current user is disabled.
    """
    logger.debug(f"Getting current active user")

    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user