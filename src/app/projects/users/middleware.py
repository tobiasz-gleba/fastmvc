from fastapi_jwt_auth import AuthJWT
from fastapi import HTTPException, Depends

def require_user(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        user_uuid = Authorize.get_jwt_subject()

    except Exception as e:
        error = e.__class__.__name__
        print(error)
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=401, detail='You are not logged in')
        if error == 'UserNotFound':
            raise HTTPException(
                status_code=401, detail='User no longer exist')
        if error == 'NotVerified':
            raise HTTPException(
                status_code=401, detail='Please verify your account')
        raise HTTPException(
            status_code=401, detail='Token is invalid or has expired')
    return user_uuid
