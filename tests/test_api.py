import pytest
from fastapi.testclient import TestClient
from pydantic import SecretStr, ValidationError
from redis.exceptions import ConnectionError as RedisConnectionError
from sqlalchemy.exc import OperationalError
from traceleaf_api.main import create_app
from traceleaf_core.config import Settings


@pytest.fixture
def settings():
    return Settings(
        _env_file=None,
        database_url=SecretStr("postgresql+psycopg://user:private-db-password@localhost/test"),
        redis_url=SecretStr("redis://localhost:6379/0"),
        model_api_key=None,
    )


def test_liveness_does_not_require_dependencies(settings):
    with TestClient(create_app(settings)) as client:
        assert client.get("/api/v1/health/live").json() == {"status": "alive"}


@pytest.mark.parametrize("database_ready,redis_ready", [(True, True), (False, True), (True, False)])
def test_readiness_reports_each_dependency(monkeypatch, settings, database_ready, redis_ready):
    monkeypatch.setattr("traceleaf_api.main.check_database", lambda _: database_ready)
    monkeypatch.setattr("traceleaf_api.main.Redis.ping", lambda _: redis_ready)
    with TestClient(create_app(settings)) as client:
        response = client.get("/api/v1/health/ready")
    assert response.status_code == (200 if database_ready and redis_ready else 503)
    assert response.json()["services"] == {"postgresql": database_ready, "redis": redis_ready}


def test_dependency_errors_do_not_expose_secrets(monkeypatch, settings):
    def broken_database(_):
        raise OperationalError("SELECT 1", {}, Exception("private-db-password"))

    def broken_redis(_):
        raise RedisConnectionError("private-redis-password")

    monkeypatch.setattr("traceleaf_api.main.check_database", broken_database)
    monkeypatch.setattr("traceleaf_api.main.Redis.ping", broken_redis)
    with TestClient(create_app(settings)) as client:
        response = client.get("/api/v1/health/ready")
    assert response.status_code == 503
    assert response.json()["services"] == {"postgresql": False, "redis": False}
    assert "private" not in response.text
    assert "private-db-password" not in repr(settings)


@pytest.mark.parametrize(
    "api_key,reason", [(None, "missing_credentials"), ("secret", "not_implemented")]
)
def test_ai_cannot_be_enabled_by_setting_a_key(settings, api_key, reason):
    settings.model_api_key = SecretStr(api_key) if api_key else None
    with TestClient(create_app(settings)) as client:
        response = client.get("/api/v1/capabilities")
    capabilities = response.json()["capabilities"]
    assert all(not value["available"] for value in capabilities.values())
    assert capabilities["rag"]["reason"] == reason
    assert "secret" not in response.text


def test_untrusted_host_is_rejected(settings):
    with TestClient(create_app(settings)) as client:
        assert (
            client.get("/api/v1/health/live", headers={"Host": "attacker.example"}).status_code
            == 400
        )


def test_missing_configuration_fails_without_exposing_inputs(monkeypatch):
    monkeypatch.delenv("TRACELEAF_DATABASE_URL", raising=False)
    monkeypatch.delenv("TRACELEAF_REDIS_URL", raising=False)
    with pytest.raises(ValidationError):
        Settings(_env_file=None)
