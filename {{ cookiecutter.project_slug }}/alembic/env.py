from __future__ import annotations

import asyncio
from logging.config import fileConfig

from databases import DatabaseURL
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


async def create_database(database_url: DatabaseURL, reset: bool = False) -> None:
    from asyncpg.exceptions import DuplicateDatabaseError
    from databases import Database

    postgres_database_url = DatabaseURL(str(database_url)).replace(database="postgres")
    database = Database(postgres_database_url)
    try:
        await database.connect()
        if reset:
            print(f"dropping {database_url.database}")
            await database.execute(f"DROP DATABASE IF EXISTS {database_url.database}")
        await database.execute(
            f"CREATE DATABASE {database_url.database}"
            f" WITH OWNER {database_url.username}"
        )
    except DuplicateDatabaseError:
        print(f"{database_url.database} exists")
    else:
        print(f"{database_url.database} created")
    finally:
        await database.disconnect()


tags = (context.get_tag_argument() or "").lower().split("_")
if "test" in tags:
    from tests.config import test_settings

    app_database_url = DatabaseURL(test_settings.TEST_APP_DATABASE_URL)
    assert app_database_url.database.startswith(
        "test"
    ), "test database name must start with 'test'"
    asyncio.run(create_database(app_database_url, reset="reset" in tags))
else:
    from app.core.config import settings

    app_database_url = DatabaseURL(settings.APP_DATABASE_URL)

print(f"using {app_database_url.obscure_password}")
config.set_main_option("sqlalchemy.url", str(app_database_url))


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
