from flask import current_app as app
from fs import open_fs
from fs_s3fs import S3FS
from os import environ as env
from functools import reduce
from urllib.parse import urlencode
from os.path import join, abspath, dirname
from collections import OrderedDict

here = abspath(dirname(__file__))


class InvalidConfigurationException(Exception):

    def __init__(self, invalid_param):
        super().__init__('Invalid Param: ' + invalid_param)


S3FS_ARGS = [
    'bucket_name',
    'dir_path',
    'aws_access_key_id',
    'aws_secret_access_key',
    'aws_session_token',
    'endpoint_url',
    'region',
    'delimiter',
    'strict',
    'cache_control',
    'acl',
    'upload_args',
    'download_args',
]


def get_env_typed(evar, default_value=None, default_type=int):
    _result = env.get(evar, default_value)
    return (default_type)(_result)


def get_config():
    cache_servers = env.get('MEMCACHED_SERVERS', '')
    cache_memcached_servers = (cache_servers.split(',')
                               if cache_servers else False)

    config = dict(
        web_database_url=env.get('WEB_DATABASE_URL', 'sqlite:////tmp/dev.db'),
        worker_database_url=env.get(
            'WORKER_DATABASE_URL', 'sqlite:////tmp/dev.db'),
        api_dealer_rater=env.get('API_DEALER_RATER', 'http://localhost:5002'),
        dealer_rater_buick=env.get(
            'DEALER_RATER_BUICK', 'http://localhost:5003'),
        use_s3=True if env.get('USE_S3', 'false').lower() == 'true' else False,
        cache_type='simple',
        cache_memcached_servers=cache_memcached_servers,
        signature_passphrase=env.get('SIGNATURE_PASSPHRASE', 'secret1105'),
        create_database=True if env.get(
            'CREATE_DATABASE', 'false').lower() == 'true' else False,
        auth_sso_provider=env.get(
            'AUTH_SSO_PROVIDER', 'da_api.auth.local.LocalSSO'),
        workflow_timeout=get_env_typed('WORKFLOW_TIMEOUT', 10 * 60),
        time_to_wait_for_service_result=get_env_typed(
            'TIME_TO_WAIT_FOR_SERVICE_RESULT', 60 * 60),
        extra_retries=get_env_typed('EXTRA_RETRIES', 0),
        lock_expire=get_env_typed('LOCK_EXPIRE', 10),
    )

    for k, v in env.items():
        if k.startswith('S3_') and not k.endswith('_PROD') and not k.endswith('_TEST'):
            if k[3:].lower() not in S3FS_ARGS:
                raise InvalidConfigurationException(k)
            config[k.lower()] = v

    if cache_memcached_servers:
        config['cache_type'] = 'memcached'
        config['cache_memcached_servers'] = cache_memcached_servers

    return config


def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def to_snake_case(camel_str):
    return reduce(lambda x, y: x + ('_' if y.isupper() else '') + y, camel_str).lower()


def dict_to_sorted_url_encoded(_dict={}):
    return urlencode(OrderedDict(sorted(_dict.items())))


def get_s3_conf(config):
    return {k.lower()[3:]: v for k, v in config.items()
            if k.lower().startswith('s3_')}


def get_bucket():
    try:
        # Used on flask context
        config = app.config
    except Exception:
        # Used on celery context
        config = get_config()

    if config.get('use_s3'):
        return S3FS(**get_s3_conf(config))
    else:
        return open_fs(abspath(join(here, '..',  'bucket')))
