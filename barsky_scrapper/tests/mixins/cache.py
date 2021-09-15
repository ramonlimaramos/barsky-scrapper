from barsky_scrapper.cache import cache
from unittest.mock import patch


__all__ = ['CacheMixin', 'BackgroundCacheMixin']


class CacheMixin(object):

    def given_cache(self, key, value):
        cache.set(key, value)

    def given_cache_does_not_have_key(self, key):
        cache.delete(key)

    def assert_cache_has_key(self, key):
        value = cache.get(key)
        self.assertIsNotNone(value)

    def assert_cache_is(self, key, value):
        actual = cache.get(key)
        self.assertEqual(value, actual)


class BackgroundCacheMixin(object):

    def background_cache_set_up(self):
        assert hasattr(self, 'app')

        cache.init_app(self.app, config={'CACHE_TYPE': 'simple'})
        self.app.config['SECRET_KEY'] = 'secret'

        class FakeCache:

            def get(self, key):
                cached = cache.get(key)
                if cached:
                    if isinstance(cached, str):
                        cached = cached.encode('utf-8')
                    assert isinstance(cached, bytes)
                    return cached

            def set(self, key, value, expire=0):
                return cache.set(key, value, timeout=expire)

            def delete(self, key):
                return cache.set(key, None)

        self.cache = FakeCache()

        self.get_memcache_workflow_patched = patch('barsky_scrapper.services.background.dealerrater_workflow.get_memcache')
        self.get_memcache_workflow = self.get_memcache_workflow_patched.start()
        self.get_memcache_workflow.return_value = self.cache

        # self.get_memcache_helper_patched = [
        #     patch('barsky_scrapper.analyser.helpers.get_memcache'),
        #     patch('barsky_scrapper.background.events.get_memcache'),
        #     patch('barsky_scrapper.background.periodic_tasks.get_memcache'),
        # ]
        # for helper_patched in self.get_memcache_helper_patched:
        #     helper = helper_patched.start()
        #     helper.return_value = self.cache

        # self.sleep_patched = patch('barsky_scrapper.analyser.helpers.sleep')
        # self.sleep = self.sleep_patched.start()

    def background_cache_tear_down(self):
        self.get_memcache_workflow_patched.stop()
        # for helper_patched in self.get_memcache_helper_patched:
        #     helper_patched.stop()
        # self.sleep_patched.stop()
