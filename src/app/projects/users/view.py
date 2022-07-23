from fastapi import APIRouter, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT
from .schema import User
from .dependency import get_current_user
from core.db import Command, Query, select
from .utils import get_hashed_password, verify_password

app = APIRouter()

@app.post('/login')
async def login(user: User, Authorize: AuthJWT = Depends()):
    Authorize.unset_jwt_cookies()

    user_from_db = await Query(select(User).where(User.username == user.username).limit(1)).get_async_result()
    if user_from_db == []:
        raise HTTPException(404)
    else:
        user_from_db = user_from_db[0]

    if user.username != user_from_db.username or True != verify_password(user.password ,user_from_db.password):
        raise HTTPException(status_code=401, detail="Bad username or password")

    # Create the tokens and passing to set_access_cookies or set_refresh_cookies
    access_token = Authorize.create_access_token(subject=user.username)
    refresh_token = Authorize.create_refresh_token(subject=user.username)

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
    """
    Because the JWT are stored in an httponly cookie now, we cannot
    log the user out by simply deleting the cookies in the frontend.
    We need the backend to send us a response to delete the cookies.
    """
    Authorize.jwt_required()

    Authorize.unset_jwt_cookies()
    return {"msg":"Successfully logout"}


@app.post('/register')
async def refresh(user: User):
    db_query = await Query(select(User).where(User.username == user.username)).get_async_result()

    if len(db_query) == 0:
        user.password = get_hashed_password(user.password)
        user = await Command().insert(user)
    else:
        raise HTTPException(status_code = 409)

    return user


@app.get('/protected')
async def protected(user: User = Depends(get_current_user)):
    """
    We do not need to make any changes to our protected endpoints. They
    will all still function the exact same as they do when sending the
    JWT in via a headers instead of a cookies
    """    
    return user