from sqlmodel import SQLModel
from sqlmodel import Field, SQLModel
from typing import Optional
import uuid as uuid_pkg
from sqlmodel import SQLModel, Field
from pydantic import EmailStr

class User(SQLModel, table=True):
    uuid: Optional[uuid_pkg.UUID] = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    email: EmailStr
    password: str
