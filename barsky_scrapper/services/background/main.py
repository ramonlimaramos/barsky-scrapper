from celery import Celery, Task
from os import environ as env
from celery.signals import after_setup_logger

from http.client import RemoteDisconnected
from psycopg2 import OperationalError

from barsky_scrapper.domain import db_session
from sqlalchemy import create_engine

from requests.exceptions import ConnectionError as RequestsConnectionError
from redis.exceptions import ConnectionError as RedisConnectionError

from barsky_scrapper.helper import get_config


__all__ = ['create_celery', 'DBTask', 'AUTORETRY_FOR', 'is_feature_active', 'app']


vars_config = get_config()


AUTORETRY_FOR = (RemoteDisconnected,
                 RequestsConnectionError,
                 OperationalError,
                 RedisConnectionError,
                 )


def is_feature_active(feature):
    return env.get(f'TOOGLE_{feature}'.upper()) == '1'


class DBTask(Task):
    _db_session = None
    _db_engine = None

    def after_return(self, *args, **kwargs):
        if self._db_session is not None:
            self._db_session.remove()
            if self._db_engine is not None:
                self._db_engine.dispose()

    def get_db_session(self):
        """
        this method return a scoped_session configured session with postgreSQL database
        :return: scoped_session
        """
        if self._db_session is None:
            api_database_uri = vars_config['worker_database_url']
            self._db_engine = create_engine(api_database_uri, convert_unicode=True)
            db_session.configure(bind=self._db_engine)
            self._db_session = db_session
        return self._db_session


def create_celery():
    worker = Celery('barsky_scrapper')

    worker.config_from_object('barsky_scrapper.services.background.config')
    worker.autodiscover_tasks(['barsky_scrapper.services.background.dealerrater_workflow'])

    return worker


app = create_celery()