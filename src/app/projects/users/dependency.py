from .schema import User
from fastapi import Depends
from fastapi_jwt_auth import AuthJWT
from core.db import Query, select
from fastapi import HTTPException

async def get_current_user(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user_from_db = Query(select(User).where(User.email == current_user).limit(1)).get_result()
    if user_from_db == []:
        Authorize.unset_jwt_cookies()
        raise HTTPException(401)
    user = user_from_db[0]
    user.password = None
    return user