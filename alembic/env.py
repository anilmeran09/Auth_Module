from logging.config import fileConfig
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.engine import Connection
import os
import sys
import asyncio

# Add project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Alembic config
config = context.config
fileConfig(config.config_file_name)

# Import Base and models (VERY IMPORTANT)
from db.base import Base
import db.models  # noqa: F401  <-- registers all models

target_metadata = Base.metadata

# Async engine (simple + correct)
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)

def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection: Connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
