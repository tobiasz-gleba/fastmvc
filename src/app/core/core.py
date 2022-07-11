from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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



for router_item in routers:
    router, prefix, tags = router_item

    if tags:
        app_core.include_router(router, prefix=f"/{prefix}", tags=tags)
    else:
        app_core.include_router(router, prefix=f"/{prefix}")