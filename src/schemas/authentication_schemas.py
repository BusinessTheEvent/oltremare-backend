import datetime
from pydantic import BaseModel, SecretStr


## TODO: Change all password type to SecretStr if needed

class RoleBase(BaseModel):
    id: int
    name: str
    scopes: str

class GroupBase(BaseModel):
    id: int
    name: str
    scopes: str

    class Config:
        from_attributes = True

class GroupRequest(BaseModel):
    name: str
    scopes: str   

class GroupBaseList(BaseModel):
    groups: list[GroupBase]

class UserUsername(BaseModel):
    username: str

class UserBase(BaseModel):
    username: str
    name: str
    is_active: bool
    disabled: bool
    groups: list[GroupBase]
    additional_scopes: str
    role: RoleBase
    is_application: bool

    class Config:
        from_attributes = True

class UserRegister(UserBase):
    groups: list[str]
    role: str
    password: SecretStr
    password_confirm: SecretStr

class UserResponse(BaseModel):
    username: str
    name: str
    is_active: bool
    disabled: bool
    groups: list[GroupBase]
    additional_scopes: str
    role: RoleBase
    registered_at: datetime.datetime
    last_login: datetime.datetime | None
    date_init_validity: datetime.datetime | None
    date_end_validity: datetime.datetime | None
    
    class Config:
        from_attributes = True

class UserWithPassword(UserBase):
    all_scopes: str
    password: SecretStr

class Token(BaseModel):
    auth_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []

class PasswordResetRequest(BaseModel):
    old_password: SecretStr
    new_password: SecretStr
    new_password_confirm: SecretStr

class UserScopes(BaseModel):
    username: str
    role_scopes: str
    additional_scopes: str
    group_scopes: str | None = None
    all_scopes: str

class UserAdditionalScopes(BaseModel):
    username: str
    additional_scopes: str

class GetScopesRequest(BaseModel):
    username: str

class ModifyPermissionRequest(BaseModel):
    username: str
    additional_scopes: list[str] | None = None

class UserGroups(BaseModel):
    username: str
    groups: list[GroupBase]

class UserGroupsRequest(BaseModel):
    username: str

class UserGroupsModifyRequest(BaseModel):
    username: str
    groups: list[str]