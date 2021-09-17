from barsky_scrapper.helper import get_config

try:
    from pymemcache.client.base import Client as Memcache
except ImportError:
    class Memcache:

        def __init__(self, *args, **kwargs):
            raise Exception


class CacheNotConfigured(Exception):
    pass


def get_memcache():
    config = get_config()

    cache_type = config.get('cache_type')
    if cache_type == 'memcached':
        return Memcache((','.join(config['cache_memcached_servers']), 11211))
    else:
        raise CacheNotConfigured()
