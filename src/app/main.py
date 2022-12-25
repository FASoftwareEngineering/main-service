import copy
import sys

import sentry_sdk
import uvicorn
from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from app import api
from app.config import Config, config
from app.core.db import db


def create_app(conf: Config) -> FastAPI:
    app = FastAPI()

    configure_logging(conf)
    add_middlewares(app, conf)
    delayed_configuration(conf)
    include_routers(app, conf)

    return app


def configure_logging(conf: Config) -> None:
    log_conf = copy.deepcopy(conf.LOGGING_CONFIG)

    if "handlers" in log_conf:
        sinks = {
            "sys.stderr": sys.stderr,
            "sys.stdout": sys.stdout,
        }
        for h in log_conf.get("handlers"):
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


def delayed_configuration(conf: Config) -> None:
    db.configure(conf)
    sentry_sdk.init(dsn=conf.SENTRY_DSN, traces_sample_rate=1)


def include_routers(app: FastAPI, conf: Config) -> None:
    app.include_router(api.router, prefix=conf.API_PREFIX)


app = create_app(config)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True, use_colors=True)
