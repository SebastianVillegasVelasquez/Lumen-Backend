import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from src.core.config import settings
from src.db.base import Base

# Import the model here to ensure they are registered with Alembic

"""
The following imports are required for Alembic to work properly.
Do not change the imports if you are not sure what they do.
"""


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

if not settings.DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable must be set for migrations")


def run_migrations_offline() -> None:
    database_url = settings.DATABASE_URL
    if not database_url:
        raise ValueError("DATABASE_URL is required for offline migrations")
    context.configure(
        url=database_url,
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


async def run_async_migrations() -> None:
    # Retrieve the section from the alembic.ini file
    section = config.get_section(config.config_ini_section, {})

    # Validate DATABASE_URL before use
    database_url = settings.DATABASE_URL
    if not database_url:
        raise ValueError("DATABASE_URL is required for async migrations")

    # Inject the URL from the .env file into the configuration
    section["sqlalchemy.url"] = database_url

    connectable = async_engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
