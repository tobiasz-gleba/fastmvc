from fastapi import APIRouter, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT
from .schema import User
from .dependency import get_current_user
from core.db import Command, Query, select
from utils.base import get_hashed_password, verify_password

app = APIRouter()

@app.post('/login')
async def login(user: User, Authorize: AuthJWT = Depends()):
    # logout user
    Authorize.unset_jwt_cookies()

    # check if user exists in database
    user_from_db = await Query(select(User).where(User.email == user.email).limit(1)).get_async_result()
    if user_from_db == []:
        raise HTTPException(404)
    else:
        user_from_db = user_from_db[0]

    if user.email != user_from_db.email or True != verify_password(user.password ,user_from_db.password):
        raise HTTPException(status_code=401, detail="Bad email or password")

    # Create the tokens and passing to set_access_cookies or set_refresh_cookies
    access_token = Authorize.create_access_token(subject=user.email)
    refresh_token = Authorize.create_refresh_token(subject=user.email)
    # Set the JWT cookies in the response
    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    return {"msg":"Successfully login"}


@app.post('/refresh')
async def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    # Set the JWT cookies in the response
    Authorize.set_access_cookies(new_access_token)
    return {"msg":"The token has been refresh"}


@app.delete('/logout')
async def logout(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    Authorize.unset_jwt_cookies()
    return {"msg":"Successfully logout"}


@app.post('/register')
async def register(user: User, Authorize: AuthJWT = Depends()):
    # logout user
    Authorize.unset_jwt_cookies()
    # check if user exists in database
    db_query = await Query(select(User).where(User.email == user.email)).get_async_result()
    if len(db_query) == 0:
        # valid_password() #TODO 
        user.password = get_hashed_password(user.password)
        user.uuid = None
        user = await Command().insert(user)
    else:
        raise HTTPException(status_code = 409)

    return user


@app.get('/me')
async def protected(user: User = Depends(get_current_user)):
    return user