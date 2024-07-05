import datetime
import pprint
from typing import Annotated, Union
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.config import settings
from .models import Group, Role, User
from .security import authenticate_user, create_access_token, get_current_active_user, get_password_hash, verify_password
from ..databases.db import get_auth_db
from ..schemas import authentication_schemas
from ..default_logger import get_custom_logger
from fastapi.security import OAuth2PasswordRequestForm



router = APIRouter()
logger = get_custom_logger(__name__)

## remember to set role dynamically when creating users
@router.post("/register", response_model=authentication_schemas.UserResponse, tags=["User management"])
def register(user_data: authentication_schemas.UserRegister, db: Annotated[Session, Depends(get_auth_db)]) -> authentication_schemas.UserResponse:

    logger.debug(f"Registering user {user_data.username}")

    if db.query(User).filter(User.username == user_data.username).first() is not None:
        logger.error(f"User with username {user_data.username} already exists")
        raise HTTPException(status.HTTP_409_CONFLICT, detail=f"User with username {user_data.username} already exists")

    if user_data.password.get_secret_value() != user_data.password_confirm.get_secret_value():
        logger.error(f"Passwords do not match")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Passwords do not match")
    else:
        new_user = User(
            username=user_data.username,
            name=user_data.name,
            password=get_password_hash(user_data.password.get_secret_value()),
            is_active=user_data.is_active,
            disabled=user_data.disabled,
            additional_scopes=user_data.additional_scopes,
            registered_at=datetime.datetime.now(),
            is_application=user_data.is_application
        )

        role = db.query(Role).filter(Role.name == user_data.role.upper()).first()
        if role is None:
            logger.error(f"Role {user_data.role} not found")
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Role {user_data.role} not found")
        new_user.role = role

        for group in user_data.groups:
            new_group = db.query(Group).filter(Group.name == group.upper()).first()
            if new_group is None:
                logger.error(f"Group {group.upper} not found")
                raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Group {new_group} not found")
            else:
                new_user.groups.append(new_group)
        
        ## check data and repair if possible
        try:
            new_user.self_check_and_repair()
        except ValueError as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

        db.add(new_user)
        db.commit()
        logger.info(f"User {new_user.username} created")

        return new_user
        
@router.post("/token", name="token", response_model=authentication_schemas.Token, tags=["User management"])
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_auth_db)]):
    
    logger.debug(f"Logging in user {form_data.username}")
    user = authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        logger.warning(f"Invalid credentials for user {form_data.username}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    else:
        logger.debug(f"User: {user.username}")
        
        to_update = db.query(User).filter(User.username == user.username).first()
        to_update.last_login = datetime.datetime.now()
        db.add(to_update)
        db.commit()

        #access_token_expires = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        access_token = create_access_token(
            data={"sub": user.username, "scopes": user.all_scopes.split(" ")} ## Inserting all the scopes from the users into the token
            #expires_delta=access_token_expires # if you want to set the expiration time manually
        )

        if settings.USE_COOKIES_AUTH:
            response =JSONResponse(content={"message": "Logged in"})
            response.set_cookie(key="auth_token", value=f"Bearer {access_token}", httponly=True, max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES*60, expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES*60, path="/")
            return response
        
        return {"auth_token": access_token, "token_type": "bearer"}
    
@router.get("/logout", tags=["User management"])
def logout():
    ## TODO: implement this route
    ## make token expire? 
    ## is there a way to do this by the state of the art?

    if settings.USE_COOKIES_AUTH:
        response = JSONResponse(content={"message": "Logged out"})
        response.set_cookie(key="auth_token", value=f"Searching for something here?", httponly=True, expires=settings.ACCESS_TOKEN_EXPIRE_NOW*60, path="/")
        #response.delete_cookie(key="auth_token", path="/")
        return response
    else:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented, yet.")
    

@router.get("/me", response_model=authentication_schemas.UserResponse, tags=["User management"])
def read_users_me(request: Request, current_user: Annotated[authentication_schemas.UserBase, Depends(get_current_active_user)], db: Annotated[Session, Depends(get_auth_db)]) -> Union[authentication_schemas.UserResponse, HTTPException]:
    
    pprint.pprint(request.cookies.get("access_token"))
    current_user = db.query(User).filter(User.username == current_user.username).first()
    
    return current_user


@router.patch('/password_reset', tags=["User management"])
def password_reset(current_user: Annotated[authentication_schemas.UserBase, Depends(get_current_active_user)], db: Annotated[Session, Depends(get_auth_db)], data: authentication_schemas.PasswordResetRequest):

    if current_user is None:
        logger.error("Problem with user authentication or in OAuth2 scheme")

    if not current_user.is_active:
        logger.warning(f"User {current_user.username} is not active")
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=f"User {current_user.username} is not active")
    
    if current_user.disabled:
        logger.warning(f"User {current_user.username} is disabled")
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=f"User {current_user.username} is disabled")
    
    user = db.query(User).filter(User.username == current_user.username).first()

    if not verify_password(data.old_password.get_secret_value(), user.password):
        logger.error("Old password is incorrect")
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Old password is incorrect")
    
    elif data.new_password_confirm.get_secret_value() != data.new_password.get_secret_value():
        logger.error("Passwords do not match")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Passwords do not match")
    
    else:
        logger.debug(f"Resetting password for user {current_user.username}")
        user.password = get_password_hash(data.new_password.get_secret_value())
        db.add(user)
        db.commit()
        logger.info(f"Password reset for user {current_user.username}")

    return {"message": "Password reset successfully"}


@router.delete("/delete", tags=["User management"])
def delete_user(current_user: Annotated[authentication_schemas.UserBase, Depends(get_current_active_user)], db: Annotated[Session, Depends(get_auth_db)], data: authentication_schemas.UserUsername):
    """
        Deletes the specified user from the database.
    """
    
    logger.info(f"User {current_user.username} requested to delete user {data.username}")

    if current_user.username == data.username:
        logger.warning(f"User {current_user.username} tried to delete himself")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot delete yourself.")

    user = db.query(User).filter(User.username == data.username).first()

    if user is None:
        logger.warning(f"User {data.username} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    else:
        db.delete(user)
        db.commit()
        logger.info(f"User {user.username} deleted by {current_user.username}")
 
        return None




@router.get('/scopes', response_model=authentication_schemas.UserScopes, tags=["Scopes management"])
def get_own_scopes(current_user: Annotated[authentication_schemas.UserBase, Depends(get_current_active_user)], db: Annotated[Session, Depends(get_auth_db)]) -> Union[HTTPException, authentication_schemas.UserScopes]:
    """
        Returns the scopes of the user 
    """

    user = db.query(User).filter(User.username == current_user.username).first()
    if user is None:
        logger.error(f"User {current_user.username} not found")
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"User {current_user.username} not found")
    else:
        role_scopes = user.role.scopes
        additional_scopes = user.additional_scopes
        if user.groups is not None:
            group_scopes = " ".join([group.scopes for group in user.groups])
        else:
            group_scopes = None
        
        all_scopes = " ".join(user.get_all_scopes()).strip()
    
    return {
        "username": user.username,
        "role_scopes": role_scopes,
        "additional_scopes": additional_scopes,
        "group_scopes": group_scopes,
        "all_scopes": all_scopes
    }


@router.post('/scopes', response_model=authentication_schemas.UserScopes, tags=["Scopes management"])
def get_scopes(current_user: Annotated[authentication_schemas.UserBase, Depends(get_current_active_user)], db: Annotated[Session, Depends(get_auth_db)], data: authentication_schemas.GetScopesRequest) -> Union[HTTPException, authentication_schemas.UserScopes]:
    """
        Returns the scopes of the specified user.
    """
    logger.info(f"User {current_user.username} requested scopes for user {data.username}")

    ## TODO: replace all db queries with a function from .crud
    user = db.query(User).filter(User.username == data.username).first()
    if user is None:
        logger.debug(f"User {data.username} not found, not showing any scopes.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    else:
        role_scopes = user.role.scopes
        additional_scopes = user.additional_scopes.strip()
        if user.groups is not None:
            group_scopes = " ".join([group.scopes for group in user.groups])
        else:
            group_scopes = None
        
        all_scopes = " ".join([role_scopes.strip(), additional_scopes.strip(), group_scopes.strip()])
    
    return {
        "username": user.username,
        "role_scopes": role_scopes,
        "additional_scopes": additional_scopes,
        "group_scopes": group_scopes,
        "all_scopes": all_scopes
    }


@router.patch('/scopes/add', response_model=authentication_schemas.UserAdditionalScopes, tags=["Scopes management"])
def add_permission(current_user: Annotated[authentication_schemas.UserBase, Depends(get_current_active_user)], db: Annotated[Session, Depends(get_auth_db)], data: authentication_schemas.ModifyPermissionRequest) -> Union[HTTPException, authentication_schemas.UserAdditionalScopes]:
    """
        Adds a scopes to the specified user.
    """
    logger.info(f"User {current_user.username} requested to add scopes to user {data.username}")

    user = db.query(User).filter(User.username == data.username).first()

    if user is not None:
        if user.username == current_user.username:
            logger.info(f"User {user.email} tried to change his own scopes.")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot change your own scopes.")

        logger.debug(f"Adding scopes {data.additional_scopes} to user {user.username}")
        user.add_additional_permission(data.additional_scopes)
        db.add(user)
        db.commit()
        
        logger.debug(f"Scopes for user {user.username} succesfully updated by {current_user.username}.")

        return user
    else:
        logger.debug(f"User {data.email} not found, not changing any scopes.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    

@router.post('/scopes/delete', response_model=authentication_schemas.UserAdditionalScopes, tags=["Scopes management"])
def remove_permission(current_user: Annotated[authentication_schemas.UserBase, Depends(get_current_active_user)], db: Annotated[Session, Depends(get_auth_db)], data: authentication_schemas.ModifyPermissionRequest) -> Union[HTTPException, authentication_schemas.UserAdditionalScopes]:
    """
    Removes a scopes from the specified user.
    """

    logger.info(f"User {current_user.username} requested to delete scopes of user {data.username}")

    user = db.query(User).filter(User.username == data.username).first()

    if user is not None:    
        if user.username == current_user.username:
            logger.info(f"User {user.username} tried to change his own scopes.")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot change your own scopes.")

        user.remove_additional_permission(data.additional_scopes)
        db.add(user)
        db.commit()

        logger.debug(f"Scopes for user {user.username} succesfully updated by {current_user.username}.")

        return user
    else:
        logger.debug(f"User {data.username} not found, not changing any scopes.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    

## GROUPS MANAGEMENT ##

@router.get('/groups', response_model=authentication_schemas.GroupBaseList, tags=["Groups management"])
def get_available_groups(current_user: Annotated[authentication_schemas.UserBase, Depends(get_current_active_user)], db: Annotated[Session, Depends(get_auth_db)]) -> Union[HTTPException, authentication_schemas.GroupBaseList]:
    """
        Returns the available groups.
    """
    groups = db.query(Group).all()
    return {"groups": groups}

    
@router.put('/groups', response_model=authentication_schemas.GroupBase, tags=["Groups management"])
def create_group(current_user: Annotated[authentication_schemas.UserBase, Depends(get_current_active_user)], db: Annotated[Session, Depends(get_auth_db)], data: authentication_schemas.GroupRequest) -> Union[HTTPException, authentication_schemas.GroupBase]:
    """
        Create a new group.
    """
    logger.info(f"User {current_user.username} requested to create group {data.name}")

    if db.query(Group).filter(Group.name == data.name.upper()).first() is not None:
        logger.error(f"Group {data.name} already exists")
        raise HTTPException(status.HTTP_409_CONFLICT, detail=f"Group {data.name} already exists")
    else:
        new_group = Group(name=data.name.upper(), scopes=data.scopes)
        db.add(new_group)
        db.commit()
        logger.info(f"Group {new_group.name} created by {current_user.username}")

        return new_group


@router.delete('/groups', tags=["Groups management"])
def delete_group(current_user: Annotated[authentication_schemas.UserBase, Depends(get_current_active_user)], db: Annotated[Session, Depends(get_auth_db)], data: authentication_schemas.GroupRequest):
    """
        Deletes the specified group from the database.
    """

    logger.info(f"User {current_user.username} requested to delete group {data.name}")

    group = db.query(Group).filter(Group.name == data.name.upper()).first()

    if group is None:
        logger.warning(f"Group {data.name} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found.")
    else:
        db.delete(group)
        db.commit()
        logger.info(f"Group {group.name} deleted by {current_user.username}")

        return None


@router.get('/groups/users', response_model=authentication_schemas.UserGroups, tags=["Groups management"])
def get_own_groups(current_user: Annotated[authentication_schemas.UserBase, Depends(get_current_active_user)], db: Annotated[Session, Depends(get_auth_db)]) -> Union[HTTPException, authentication_schemas.UserGroups]:
    """
        Returns the groups of the user 
    """
    user = db.query(User).filter(User.username == current_user.username).first()
    
    if user:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    

@router.post('/groups/users', response_model=authentication_schemas.UserGroups, tags=["Groups management"])
def get_user_groups(current_user: Annotated[authentication_schemas.UserBase, Depends(get_current_active_user)], db: Annotated[Session, Depends(get_auth_db)], data: Annotated[authentication_schemas.UserGroupsRequest, None]) -> Union[HTTPException, authentication_schemas.UserGroups]:
    """
        Returns the groups of the user 
    """

    user = db.query(User).filter(User.username == data.username).first()
    
    if user:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    

@router.patch('/groups/users/add', response_model=authentication_schemas.UserGroups, tags=["Groups management"])
def add_group(current_user: Annotated[authentication_schemas.UserBase, Depends(get_current_active_user)], db: Annotated[Session, Depends(get_auth_db)], data: Annotated[authentication_schemas.UserGroupsModifyRequest, None]) -> Union[HTTPException, authentication_schemas.UserGroups]:
    """
        Adds a group to the specified user.
    """

    logger.info(f"User {current_user.username} requested to add groups to user {data.username}")

    user = db.query(User).filter(User.username == data.username).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    
    else:
        for group in data.groups:
            new_group = db.query(Group).filter(Group.name == group.upper()).first()

            if new_group is None:
                raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Group {group.upper()} not found")
            
            elif new_group not in user.groups:
                user.groups.append(new_group)

        db.add(user)
        db.commit()

        logger.info(f"Groups for user {user.username} succesfully updated by {current_user.username}.")

        return user
    

@router.post('/groups/users/delete', response_model=authentication_schemas.UserGroups, tags=["Groups management"])
def remove_user_groups(current_user: Annotated[authentication_schemas.UserBase, Depends(get_current_active_user)], db: Annotated[Session, Depends(get_auth_db)], data: Annotated[authentication_schemas.UserGroupsModifyRequest, None]) -> Union[HTTPException, authentication_schemas.UserGroups]:
    """
        Removes a group from the specified user.
    """

    logger.info(f"User {current_user.username} requested to delete groups of user {data.username}")

    user = db.query(User).filter(User.username == data.username).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    
    else:
        for group in data.groups:
            new_group = db.query(Group).filter(Group.name == group.upper()).first()

            if new_group is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Group {group.upper()} not found")
            
            elif new_group in user.groups:
                user.groups.remove(new_group)

        db.add(user)
        db.commit()

        logger.info(f"Groups for user {user.username} succesfully updated by {current_user.username}.")

        return user