from utils.base import AppObject
from pydantic import EmailStr

class User(AppObject, table=True):
    email: EmailStr
    password: str
