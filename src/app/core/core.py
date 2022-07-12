from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from elasticapm.contrib.starlette import ElasticAPM
from utils.observability import apm
from config import config
from core.routers import routers

fast_api_args = {
    'title': config.server.SERVER_API_APP_NAME,
    'description': "Defaultmq is REST based message queue witch any database as a storage.",
    'version': config.server.SERVER_APP_VERSION,
    'docs_url': config.server.SERVER_APP_DOCS_URL,
}

app_core = FastAPI(**fast_api_args)

if config.elastic_apm.APM_ENABLED:
    app_core.add_middleware(
        ElasticAPM, 
        client=apm
    )

app_core.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['GET','PUT','POST', 'DELETE', 'PATCH'],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
private_key = """
-----BEGIN RSA PRIVATE KEY-----
MIICWwIBAAKBgGBoQhqHdMU65aSBQVC/u9a6HMfKA927aZOk7HA/kXuA5UU4Sl+U
C9WjDhMQFk1PpqAjZdCqx9ajolTYnIfeaVHcLNpJQ6QXLnUyMnfwPmwYQ2rkuy5w
I2NdO81CzJ/9S8MsPyMl2/CF9ZxM03eleE8RKFwXCxZ/IoiqN4jVNjSrAgMBAAEC
gYAnNqEUq146zx8TT6PilWpxB9inByuVaCKkdGPbsG+bfa1D/4Z44/4AUsdpx5Ra
s/hBkMRcIOsSChMAUe8xcK0DqA9Y7BIVfpma2fH/gYq6dP3dOfCxftZBF00HwIu7
5e7RWnBC8MkPnrkKdHq6ptAYlGgoSJTEQREqusDiuNG9yQJBAKQib2VhNAqgyvvi
PdmFrCqq15z9MY16WCfttuqfAaSYKHnZe1WvBKbSNW9x4Cgjfhzl9mlozlW4rob/
ttPN6e0CQQCWXbVtqmVdB5Ol9wQN7DIRc8q5F8HKQqIJAMTmwaRwNDsGRxCWMwGO
8WAlnejzYTXmrrytv6kXX8U40enJW2X3AkAI42h+5/WmgbCcVVMeHXQGV3wXn0p4
q+BsQR4/tF6laCwA9TsNl827rvR/1X3bDpj8vaNLcAaEc9zXqK9g5uy9AkATeOkw
3Xso8/075eRBhU/qkKs1Ew2GiuB+9/mHxJXt7eWi53sPaGWQRFPmKy/qrLEVQZWv
jn1wSHe65vw2lj57AkEAh04n1wrZnCha8s6crMhjggdTXI6G4FU3TGf8ssGboqs3
j5lemvyKod+u2JVKwarcKmd/gFYBOjsRm18LlZH74A==
-----END RSA PRIVATE KEY-----
"""
public_key = """
-----BEGIN PUBLIC KEY-----
MIGeMA0GCSqGSIb3DQEBAQUAA4GMADCBiAKBgGBoQhqHdMU65aSBQVC/u9a6HMfK
A927aZOk7HA/kXuA5UU4Sl+UC9WjDhMQFk1PpqAjZdCqx9ajolTYnIfeaVHcLNpJ
Q6QXLnUyMnfwPmwYQ2rkuy5wI2NdO81CzJ/9S8MsPyMl2/CF9ZxM03eleE8RKFwX
CxZ/IoiqN4jVNjSrAgMBAAE=
-----END PUBLIC KEY-----
"""
class Settings(BaseModel):
    authjwt_algorithm: str = "RS512"
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False
    authjwt_public_key: str = public_key
    authjwt_private_key: str = private_key

@AuthJWT.load_config
def get_config():
    return Settings()

@app_core.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )



app_core.mount("/static", StaticFiles(directory="static"), name="static")
for router_item in routers:
    router, prefix, tags = router_item

    if tags:
        app_core.include_router(router, prefix=f"/{prefix}", tags=tags)
    else:
        app_core.include_router(router, prefix=f"/{prefix}")