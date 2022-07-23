from fastapi import APIRouter, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT
from .schema import User
from .dependency import get_current_user
from core.db import Command, Query, select, engine, Session

app = APIRouter()

@app.post('/login')
async def login(user: User, Authorize: AuthJWT = Depends()):
    Authorize.unset_jwt_cookies()
    if user.username != "test" or user.password != "test":
        raise HTTPException(status_code=401,detail="Bad username or password")

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
    user = await Command().insert(user)
    return user


@app.get('/protected')
async def protected(user: User = Depends(get_current_user)):
    """
    We do not need to make any changes to our protected endpoints. They
    will all still function the exact same as they do when sending the
    JWT in via a headers instead of a cookies
    """    
    query = Query(select(User).where(User.username == "test"))
    result = await query.result()
    return result[0]
