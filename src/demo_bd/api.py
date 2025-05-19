"""Demo BD REST API."""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import fastapi_problem_details as problem
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from starlette_context import plugins
from starlette_context.middleware import ContextMiddleware

from demo_bd.core.config.settings import settings
from demo_bd.core.log.loguru_intercept_handling import setup_loguru_logging_intercept
from demo_bd.routes.api.http import http_api_routers_include

setup_loguru_logging_intercept(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    modules=(
        "uvicorn.error",
        "uvicorn.asgi",
        "uvicorn.access",
        "gunicorn",
        "gunicorn.access",
        "gunicorn.error",
    ),
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Handle FastAPI startup and shutdown events."""
    logger.info("🚀 Starting application")
    # Startup events:
    # - Remove all handlers associated with the root logger object.
    # for handler in logging.root.handlers:
    #     logging.root.removeHandler(handler)
    # # - Add coloredlogs' colored StreamHandler to the root logger.
    # coloredlogs.install()
    try:
        yield
        logger.info("⛔ Stopping application")
    finally:
        # Cleanup actions
        logger.info("✅ Application stopped")

    # Shutdown events.


app = FastAPI(lifespan=lifespan, title=settings.APP_TITLE, debug=settings.DEBUG, version="0.1.0")
problem.init_app(app, include_exc_info_in_response=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["X-Requested-With", "X-Request-ID", "X-Correlation-ID"],
    expose_headers=["X-Request-ID", "X-Correlation-ID"],
)

app.add_middleware(
    ContextMiddleware,
    plugins=(
        plugins.RequestIdPlugin(force_new_uuid=False, validate=False),
        plugins.CorrelationIdPlugin(force_new_uuid=False, validate=False),
    ),
)

http_api_routers_include(app=app)
