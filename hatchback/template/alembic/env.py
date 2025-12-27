from logging.config import fileConfig
from os import environ as env

from sqlalchemy import engine_from_config, pool

from alembic import context
from app.config.database import Base, validate_database
import app.models  # Import models to register them with Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Load environment variables if not already loaded
from dotenv import load_dotenv
load_dotenv()

db_user_name = env.get("DATABASE_USERNAME", "postgres")
db_password = env.get("DATABASE_PASSWORD", "postgres")
db_host = env.get("DATABASE_HOSTNAME", "localhost")
db_port = env.get("DATABASE_PORT", "5432")
db_name = env.get("DATABASE_NAME", "boilerplate_db")

config.set_main_option(
    "sqlalchemy.url",
    f"postgresql+psycopg2://{db_user_name}:{db_password}@{db_host}:{db_port}/{db_name}",
)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Ensure database exists
    validate_database()
    
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
