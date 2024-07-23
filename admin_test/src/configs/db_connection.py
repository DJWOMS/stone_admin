from functools import lru_cache

from esmerald.conf import settings
from edgy import Database, Registry


def db_connection() -> tuple[Database, Registry]:
    database = Database("sqlite+aiosqlite:///example.db")
    return database, Registry(database=database)


@lru_cache()
def get_db_connection_edgy():
    database, registry = db_connection()
    return database, registry


@lru_cache()
def get_db_connection():
    database, registry = settings.db_connection
    return database, registry
