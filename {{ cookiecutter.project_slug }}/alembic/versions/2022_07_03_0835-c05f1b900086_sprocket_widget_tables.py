"""sprocket, widget tables

Revision ID: c05f1b900086
Revises: c08e111136e7
Create Date: 2022-07-03 08:35:39.061483

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "c05f1b900086"
down_revision = "c08e111136e7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    sql_statements = [
        """
CREATE TABLE IF NOT EXISTS widget (
    uuid UUID PRIMARY KEY,
    created TIMESTAMPTZ NOT NULL default CURRENT_TIMESTAMP,
    updated TIMESTAMPTZ NOT NULL default CURRENT_TIMESTAMP,
    name TEXT
)
        """,
        """
CREATE TRIGGER update_timestamp
    BEFORE UPDATE on widget
    FOR EACH ROW
    EXECUTE PROCEDURE update_timestamp_trigger();
        """,
        """
CREATE TABLE IF NOT EXISTS sprocket (
    uuid UUID PRIMARY KEY,
    created TIMESTAMPTZ NOT NULL default CURRENT_TIMESTAMP,
    updated TIMESTAMPTZ NOT NULL default CURRENT_TIMESTAMP,
    teeth INTEGER NOT NULL default 0,
    widget_uuid UUID NOT NULL REFERENCES widget(uuid) ON DELETE CASCADE
);
        """,
        """
CREATE TRIGGER update_timestamp
    BEFORE UPDATE on sprocket
    FOR EACH ROW
    EXECUTE PROCEDURE update_timestamp_trigger();
        """,
    ]
    conn = op.get_bind()
    for sql in sql_statements:
        conn.execute(sa.sql.text(sql))


def downgrade() -> None:
    sql_statements = [
        """
DROP TABLE IF EXISTS widget CASCADE;
        """,
        """
DROP TABLE IF EXISTS sprocket CASCADE;
        """,
    ]
    conn = op.get_bind()
    for sql in sql_statements:
        conn.execute(sa.sql.text(sql))
