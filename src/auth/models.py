import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, DateTime
from sqlalchemy.orm import relationship
import json
from ..databases.db import Base
import re

### SQLAlchemy custom ORM models ###

# Association table
user_group_table = Table('user_group', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('group_id', Integer, ForeignKey('groups.id'))
)

## TODO: insert date init and end validity of all roles etc

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    name = Column(String, unique=False)
    surname = Column(String, unique=False)
    birthdate = Column(DateTime, nullable=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    disabled = Column(Boolean, default=False)
    additional_scopes = Column(String, default="")
    role_id = Column(Integer, ForeignKey('roles.id'))
    registered_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    last_login = Column(DateTime, nullable=True)
    is_application = Column(Boolean, default=False)
    date_init_validity = Column(DateTime, nullable=True)
    date_end_validity = Column(DateTime, nullable=True)


    role = relationship("Role", back_populates="users")
    groups = relationship("Group", secondary=user_group_table, back_populates="users")

    
    def __init__(self, **kwargs):
        self.username = kwargs.get('username')
        self.name = kwargs.get('name')
        self.password = kwargs.get('password')
        self.is_active = kwargs.get('is_active')
        self.additional_scopes = kwargs.get('additional_scopes')
        self.disabled = kwargs.get('disabled')
        self.registered_at = kwargs.get('registered_at')
        self.date_init_validity = datetime.datetime.now()
        self.date_end_validity = kwargs.get('date_end_validity', None)
        

    def self_check_and_repair(self):

        ## username checks
        if self.username is None or self.username == "":
            raise ValueError("email as username is required")
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if bool(re.match(pattern, self.username)) is False:
            raise ValueError("Invalid email format for username")
    
        ## other fields checks
        if self.name is None or self.name == "":
            raise ValueError("Name is required")
        if self.password is None or self.password == "":
            raise ValueError("Password is required")
        if self.is_active is None or not isinstance(self.is_active, bool):
            self.is_active = False
        if self.additional_scopes is None:
            self.additional_scopes = ""
        if self.disabled is None or not isinstance(self.disabled, bool):
            self.disabled = False
        if self.registered_at is None:
            self.registered_at = datetime.datetime.now()
        if self.date_init_validity is None:
            self.date_init_validity = datetime.datetime.now()

        if self.role is None or self.role == "":
            raise ValueError("Role is required to be setted")
    
    def add_additional_scope(self, new_scopes: list[str]):

        unique = []
        for perm in new_scopes:
            if perm not in self.additional_scopes:
                unique.append(perm)

        self.additional_scopes = self.additional_scopes.strip() + " " + " ".join(unique).strip()

        return self
    
    def remove_additional_scopes(self, scopes: list[str]):
        
        for perm in scopes:
            self.additional_scopes = self.additional_scopes.replace(perm.strip(), "").strip()

        return self
    
    def get_all_scopes(self) -> list:
        perms = set(self.additional_scopes.split(" "))

        for group in self.groups:
            perms = perms.union(set(group.scopes.split(" ")))

        perms = perms.union(set(self.role.scopes.split(" ")))
        perms = list(filter(None, perms))

        return perms


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    scopes = Column(String, default="")

    users = relationship("User", back_populates="role")



    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.scopes = kwargs.get('scopes')
        ## check data and repair if possible
        self.self_check_and_repair()

    def self_check_and_repair(self):
        if self.name is None or self.name == "":
            raise ValueError("Name is required")
        if self.scopes is None:
            self.scopes = ""

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'scopes': self.scopes
        }
    
    def to_json_str(self):
        return json.dumps(self.to_json())

    def from_json(self, **kwargs):
        self.name = kwargs.get['name']
        self.scopes = kwargs.get['scopes']
        ## check data and repair if possible
        self.self_check_and_repair()

        return self
    
    def add_scope(self, new_scopes: str):

        unique = []
        for perm in new_scopes.split(" "):
            if perm not in self.scopes:
                unique.append(perm)

        self.scopes = self.scopes.strip() + " " + " ".join(unique).strip()

        return self
    
    def remove_scope(self, scopes: str):
        self.scopes = self.scopes.replace(scopes.strip(), "").strip()

        return self
    
    def get_scopes(self) -> list:
        perms = set(self.scopes.split(" "))

        return list(perms)


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    scopes = Column(String, default="")

    users = relationship("User", secondary=user_group_table, back_populates="groups")

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.scopes = kwargs.get('scopes')
        ## check data and repair if possible
        self.self_check_and_repair()

    def self_check_and_repair(self):
        if self.name is None or self.name == "":
            raise ValueError("Name is required")
        if self.scopes is None:
            self.scopes = ""

    def add_scopes(self, new_scopes: str):

        unique = []
        for perm in new_scopes.split(" "):
            if perm not in self.scopes:
                unique.append(perm)

        self.scopes = self.scopes.strip() + " " + " ".join(unique).strip()

        return self
    
    def remove_scopes(self, scopes: str):
        self.scopes = self.scopes.replace(scopes.strip(), "").strip()

        return self
    
    def get_scopes(self) -> list:
        perms = set(self.scopes.split(" "))

        return list(perms)
    