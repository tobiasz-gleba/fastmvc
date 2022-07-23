from sqlmodel import SQLModel
from sqlmodel import Field, SQLModel
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str

# https://github.com/tiangolo/sqlmodel/issues/140
# from sqlmodel import SQLModel
# from sqlmodel import Field, SQLModel
# from typing import Optional
# import uuid as uuid_pkg
# from sqlmodel import SQLModel, Field


# class User(SQLModel, table=True):
#     id: Optional[uuid_pkg.UUID] = Field(
#         default_factory=uuid_pkg.uuid4,
#         primary_key=True,
#         index=True,
#         nullable=False,
#     )
#     username: str
#     password: str
