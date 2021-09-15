from __future__ import with_statement

from logging.config import fileConfig

from sqlalchemy import create_engine
from os import environ

from alembic import context

# Handles with pythonpath ModuleNotFoundError
import sys
sys.path = ['', '..'] + sys.path[1:]

from barsky_scrapper.domain import Base

from urllib.parse import urlparse, parse_qs
import alembic_autogenerate_enums

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_url():
    url = config.get_main_option("sqlalchemy.url")
    return environ.get('WEB_DATABASE_URL', url)


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()

    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    url = get_url()
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    con_args = {}
    if 'sslmode' in query:
        con_args['sslmode'] = query['sslmode'][0]

    connectable = create_engine(url, connect_args=con_args)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
