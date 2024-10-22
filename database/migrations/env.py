# database/migrations/env.py

from __future__ import with_statement
import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Adjust the path to include the project root to ensure models can be imported
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, PROJECT_ROOT)

# Import your models and DATABASE_URL
from shared.models import db  # Adjust based on your models location
from shared.utils import DATABASE_URL

# Alembic Config object, which provides access to values within the .ini file in use.
config = context.config

# Update the path to the alembic.ini file
alembic_ini_path = os.path.join(os.path.dirname(__file__), 'alembic.ini')

# Interpret the config file for Python logging.
fileConfig(alembic_ini_path)

# Set target_metadata for 'autogenerate' support
target_metadata = db.metadata

def get_url():
    return DATABASE_URL

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
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