from .schema import User
from fastapi import Depends
from fastapi_jwt_auth import AuthJWT

def get_current_user(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user = User(username=current_user, password="test")
    return user