"""Run only against a disposable *_test database, never the development workspace."""

import os

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from pydantic import SecretStr
from redis import Redis
from sqlalchemy import make_url, text
from traceleaf_api.main import create_app
from traceleaf_core.config import Settings
from traceleaf_core.database import create_database_engine

pytestmark = pytest.mark.integration


def test_migration_roundtrip_vector_and_real_readiness(monkeypatch):
    url = os.getenv("TRACELEAF_INTEGRATION_DATABASE_URL")
    if not url:
        pytest.skip(
            "Use make integration with its isolated database; real services were not tested"
        )
    assert (make_url(url).database or "").endswith("_test"), "Refusing a non-test database"
    redis_url = os.environ["TRACELEAF_INTEGRATION_REDIS_URL"]
    monkeypatch.setenv("TRACELEAF_DATABASE_URL", url)
    monkeypatch.setenv("TRACELEAF_REDIS_URL", redis_url)
    settings = Settings(_env_file=None, database_url=SecretStr(url), redis_url=SecretStr(redis_url))
    config = Config("alembic.ini")
    engine = create_database_engine(settings)
    try:
        command.downgrade(config, "base")
        with TestClient(create_app(settings)) as client:
            assert client.get("/api/v1/health/ready").status_code == 503
            command.upgrade(config, "head")
            command.upgrade(config, "head")  # A second startup is safe.
            response = client.get("/api/v1/health/ready")
            assert response.status_code == 200
            assert response.json()["services"] == {"postgresql": True, "redis": True}
            with engine.connect() as connection:
                assert (
                    connection.execute(text("SELECT '[1,2]'::vector <-> '[1,2]'::vector")).scalar()
                    == 0
                )
            command.downgrade(config, "base")
            assert client.get("/api/v1/health/ready").status_code == 503
            command.upgrade(config, "head")
            assert client.get("/api/v1/health/ready").status_code == 200
        with Redis.from_url(redis_url) as redis:
            assert redis.ping()
    finally:
        engine.dispose()
