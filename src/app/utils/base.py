from sqlmodel import Field, SQLModel
from typing import Optional
import uuid as uuid_pkg
from sqlmodel import SQLModel, Field

class AppObject(SQLModel):
    uuid: Optional[uuid_pkg.UUID] = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )