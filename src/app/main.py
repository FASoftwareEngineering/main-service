import copy
import sys

import uvicorn
from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from app import api
from app.config import Config, config
from app.models import *  # noqa: F401


def create_app(conf: Config) -> FastAPI:
    app = FastAPI()

    configure_logging(conf)
    add_middlewares(app, conf)
    include_routers(app, conf)

    return app


def configure_logging(conf: Config) -> None:
    log_conf = copy.deepcopy(conf.LOGGING_CONFIG)

    if "handlers" in log_conf:
        sinks = {
            "sys.stderr": sys.stderr,
            "sys.stdout": sys.stdout,
        }
        for h in log_conf["handlers"]:
            h["sink"] = sinks.get(h["sink"], h["sink"])

    logger.configure(**log_conf)


def add_middlewares(app: FastAPI, conf: Config) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=conf.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def include_routers(app: FastAPI, conf: Config) -> None:
    app.include_router(api.router, prefix=conf.API_PREFIX)


app = create_app(config)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, use_colors=True)
