# app/migrations/env.py

from __future__ import with_statement
import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.base import Base
from app.core.config import settings
from app.database import async_engine, create_async_engine

config = context.config
fileConfig(config.config_file_name)
config.set_main_option('sqlalchemy.url', settings.SYNC_DATABASE_URL)
target_metadata = Base.metadata

def run_migrations_offline():
    """Exécuter les migrations en mode 'offline'."""
    url = settings.SYNC_DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Exécuter les migrations en mode 'online'."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
