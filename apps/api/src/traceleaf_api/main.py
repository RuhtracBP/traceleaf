from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI, Response
from pydantic import BaseModel
from redis import Redis
from redis.backoff import NoBackoff
from redis.exceptions import RedisError
from redis.retry import Retry
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.trustedhost import TrustedHostMiddleware
from traceleaf_core.config import Settings
from traceleaf_core.database import check_database, create_database_engine


class Readiness(BaseModel):
    status: Literal["ready", "unavailable"]
    services: dict[str, bool]


class Capability(BaseModel):
    available: bool = False
    reason: Literal["not_implemented", "missing_credentials"]
    milestone: str


class Capabilities(BaseModel):
    milestone: Literal["M0"] = "M0"
    capabilities: dict[str, Capability]


def create_app(settings: Settings | None = None) -> FastAPI:
    config = settings or Settings()  # type: ignore[call-arg]
    engine = create_database_engine(config)
    redis: Redis = Redis.from_url(
        config.redis_url.get_secret_value(),
        socket_timeout=2,
        socket_connect_timeout=2,
        retry=Retry(NoBackoff(), 0),
    )

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        try:
            yield
        finally:
            redis.close()
            engine.dispose()

    app = FastAPI(title="Traceleaf", version="0.1.0", lifespan=lifespan)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=config.allowed_hosts)

    @app.get("/api/v1/health/live")
    def live() -> dict[str, str]:
        return {"status": "alive"}

    @app.get("/api/v1/health/ready", response_model=Readiness)
    def ready(response: Response) -> Readiness:
        services = {"postgresql": False, "redis": False}
        try:
            services["postgresql"] = check_database(engine)
        except SQLAlchemyError:
            pass
        try:
            services["redis"] = bool(redis.ping())
        except RedisError:
            pass
        healthy = all(services.values())
        response.status_code = 200 if healthy else 503
        return Readiness(status="ready" if healthy else "unavailable", services=services)

    @app.get("/api/v1/capabilities", response_model=Capabilities)
    def capabilities() -> Capabilities:
        ai_reason: Literal["not_implemented", "missing_credentials"] = (
            "not_implemented" if config.model_api_key else "missing_credentials"
        )
        return Capabilities(
            capabilities={
                "markdown": Capability(reason="not_implemented", milestone="M1"),
                "text_search": Capability(reason="not_implemented", milestone="M2"),
                "rag": Capability(reason=ai_reason, milestone="M2"),
                "proposals": Capability(reason=ai_reason, milestone="M3"),
            }
        )

    return app
