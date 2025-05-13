from logging.config import fileConfig
import os
import sys

from starlette.routing import Host

from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import dotenv_values

# -----------------------
# Configure logging
# -----------------------
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# -----------------------
# Set DB URL dynamically
# -----------------------
db_url = os.getenv("DB_URL")
if not db_url:
    print("[DEBUG] Using .env values in alembic")
    env = dotenv_values(".env")
    USER = env["DB_USER"]
    PASSWORD = env["DB_PASSWORD"]
    PORT = env["DB_PORT"]
    HOST = env["DB_ACCESS"]
    DB_NAME = env["DB_NAME"]

    db_url = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
    os.environ["DB_URL"] = db_url
config.set_main_option("sqlalchemy.url", db_url)

# -----------------------
# Fix Python path for import
# (so 'backend' is importable)
# -----------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

# -----------------------
# Import Base and Models
# -----------------------
from backend.app.shared_models.sqla_base_model import Base

# Import all models to ensure they are registered with Base
from backend.app import orm

target_metadata = Base.metadata

# -----------------------
# Run offline migrations
# -----------------------
def run_migrations_offline() -> None:
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

# -----------------------
# Run online migrations
# -----------------------
def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()

# -----------------------
# Execute the correct mode
# -----------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
