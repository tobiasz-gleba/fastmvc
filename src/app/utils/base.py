from sqlmodel import Field, SQLModel
from typing import Optional
import uuid as uuid_pkg
from sqlmodel import SQLModel, Field
from passlib.context import CryptContext

class AppObject(SQLModel):
    uuid: Optional[uuid_pkg.UUID] = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)

def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)