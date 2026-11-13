from alembic import context
from traceleaf_core.config import Settings
from traceleaf_core.database import create_database_engine


def run_migrations() -> None:
    # The URL is never interpolated into an INI file or printed to logs.
    engine = create_database_engine(Settings())  # type: ignore[call-arg]
    try:
        with engine.connect() as connection:
            context.configure(connection=connection, target_metadata=None)
            with context.begin_transaction():
                context.run_migrations()
    finally:
        engine.dispose()


run_migrations()
