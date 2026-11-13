from pathlib import Path

from alembic.script import ScriptDirectory
from sqlalchemy import Engine, create_engine, text

from traceleaf_core.config import Settings

MIGRATIONS_PATH = Path(__file__).parent / "migrations"


def create_database_engine(settings: Settings) -> Engine:
    return create_engine(
        settings.database_url.get_secret_value(),
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=5,
        pool_timeout=2,
        connect_args={"connect_timeout": 2, "options": "-c statement_timeout=2000"},
        hide_parameters=True,
    )


def check_database(engine: Engine) -> bool:
    """A reachable database is not ready until its schema and vector extension are ready."""
    expected = ScriptDirectory(str(MIGRATIONS_PATH)).get_current_head()
    with engine.connect() as connection:
        revisions = (
            connection.execute(text("SELECT version_num FROM alembic_version")).scalars().all()
        )
        vector = connection.execute(
            text("SELECT extversion FROM pg_extension WHERE extname = 'vector'")
        ).scalar_one_or_none()
    return revisions == [expected] and vector is not None
