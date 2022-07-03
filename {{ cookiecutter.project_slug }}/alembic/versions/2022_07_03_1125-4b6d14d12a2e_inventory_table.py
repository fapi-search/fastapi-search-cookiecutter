"""inventory table

Revision ID: 4b6d14d12a2e
Revises: c05f1b900086
Create Date: 2022-07-03 11:25:35.616193

"""
from __future__ import annotations

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "4b6d14d12a2e"
down_revision = "c05f1b900086"
branch_labels = None
depends_on = None


def upgrade() -> None:
    sql_statements = [
        """
CREATE TABLE IF NOT EXISTS inventory (
    widget_uuid UUID PRIMARY KEY REFERENCES widget(uuid) ON DELETE CASCADE,
    created TIMESTAMPTZ NOT NULL default CURRENT_TIMESTAMP,
    updated TIMESTAMPTZ NOT NULL default CURRENT_TIMESTAMP,
    widget_count INTEGER NOT NULL default 0
)
        """,
        """
CREATE TRIGGER update_timestamp
    BEFORE UPDATE on inventory
    FOR EACH ROW
    EXECUTE PROCEDURE update_timestamp_trigger();
        """,
    ]
    conn = op.get_bind()
    for sql in sql_statements:
        conn.execute(sa.sql.text(sql))


def downgrade() -> None:
    sql = """
DROP TABLE IF EXISTS inventory CASCADE;
    """
    conn = op.get_bind()
    conn.execute(sa.sql.text(sql))
