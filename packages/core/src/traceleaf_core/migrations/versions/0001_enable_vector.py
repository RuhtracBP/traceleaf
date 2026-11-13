"""Enable vector support; document and identity tables belong to M1."""

from alembic import op

revision = "0001_enable_vector"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")


def downgrade() -> None:
    # Shared infrastructure: never drop the extension (or vector data) on rollback.
    pass
