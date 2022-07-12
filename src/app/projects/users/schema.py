from sqlmodel import SQLModel

class User(SQLModel):
    username: str
    password: str