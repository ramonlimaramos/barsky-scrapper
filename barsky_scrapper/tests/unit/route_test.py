from unittest import TestCase

from flask import Flask

from barsky_scrapper.tests.mixins import JsonMixin, CacheMixin
from barsky_scrapper.tests.route_spec import RouteSpec
from barsky_scrapper.api import api, swagger_doc
from barsky_scrapper.cache import cache


class RouteTest(JsonMixin, CacheMixin, RouteSpec, TestCase):

    API_VERSION = '/v1'

    def setUp(self):
        super(RouteTest, self).setUp()
        self.app = Flask(__name__)
        self.app.register_blueprint(swagger_doc)
        self.app.register_blueprint(api, url_prefix='/')

        cache.init_app(self.app, config={'CACHE_TYPE': 'simple'})
        self.app.config['SECRET_KEY'] = 'secret'

        self.client = self.app.test_client()

    def tearDown(self):
        super(RouteTest, self).tearDown()

    def when_acess_reviews(self):
        self.response = self.client.get('/reviews/buick/1')
    
    def when_acess_no_namespace(self):
        self.response = self.client.get('/')
