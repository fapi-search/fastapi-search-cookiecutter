"""update column trigger

Revision ID: c08e111136e7
Revises: 
Create Date: 2022-07-02 13:27:25.506271

"""
from alembic_utils.pg_function import PGFunction

from alembic import op

# revision identifiers, used by Alembic.
revision = "c08e111136e7"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    public_updated_timestamp_c08e111136e7 = PGFunction(
        schema="public",
        signature="update_timestamp_trigger()",
        definition="""
        RETURNS TRIGGER AS $$
        BEGIN
          NEW.updated = NOW();
          RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """,
    )
    op.create_entity(public_updated_timestamp_c08e111136e7)


def downgrade() -> None:
    public_updated_timestamp_c08e111136e7 = PGFunction(
        schema="public",
        signature="update_timestamp_trigger()",
        definition="",
    )
    op.drop_entity(public_updated_timestamp_c08e111136e7)
