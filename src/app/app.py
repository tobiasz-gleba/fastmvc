import asyncio
import uvicorn
from config import config
from core.core import app_core

print(config.server.SERVER_WORKERS)

# server startup conf
server_config = uvicorn.Config(
    app=app_core,
    host=config.server.SERVER_HOST,
    port=config.server.SERVER_EXPOSE_PORT,
    reload=config.server.SERVER_DEVELOPMENT,
    debug=config.server.SERVER_DEVELOPMENT,
    workers=config.server.SERVER_WORKERS,
    timeout_keep_alive=config.server.SERVER_TIMEOUT,
    access_log=config.server.SERVER_DEVELOPMENT,
    # log_config="config/log_conf.yaml"
)
server = uvicorn.Server(server_config)

# fastapi start async loop
if __name__ == "__main__":
    asyncio.run(server.serve())