import logging
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy_utils import create_database, database_exists

# Load environment variables from .env file
load_dotenv()

db_user_name = os.getenv("DATABASE_USERNAME", "postgres")
db_password = os.getenv("DATABASE_PASSWORD", "postgres")
db_host = os.getenv("DATABASE_HOSTNAME", "localhost")
db_port = os.getenv("DATABASE_PORT", "5432")
db_name = os.getenv("DATABASE_NAME", "boilerplate_db")
db_pool_size = int(os.getenv("DATABASE_POOL_SIZE", 10))
db_pool_size_overflow = int(os.getenv("DATABASE_POOL_SIZE_OVERFLOW", 10))


SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{db_user_name}:{db_password}@{db_host}:{db_port}/{db_name}"
)

logger = logging.getLogger()
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=db_pool_size,
    max_overflow=db_pool_size_overflow,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def validate_database():
    if not database_exists(engine.url):
        create_database(engine.url)
        logger.info(f"New database {engine.url} created")
    else:
        logger.info(f"INFO: DB named {db_name} already exists. Skipping creation")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
