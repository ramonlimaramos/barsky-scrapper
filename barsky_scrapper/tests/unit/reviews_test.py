from unittest import TestCase
from unittest.mock import patch

from barsky_scrapper.tests.mixins import (
    JsonMixin, FlaskMixin, BucketMixin, CacheMixin,
    DateTimeMixin, DealerRaterServiceMixin)

from barsky_scrapper.tests.reviews_spec import ReviewDealerRaterAPISpec, ReviewsMostSuspiciousAPISpec

from barsky_scrapper.api import api
from barsky_scrapper.cache import cache


class ReviewDealerRaterTest(
        FlaskMixin, JsonMixin, CacheMixin, BucketMixin, DateTimeMixin,
        DealerRaterServiceMixin, ReviewsMostSuspiciousAPISpec, ReviewDealerRaterAPISpec, TestCase):

    API_VERSION = '/v1'

    def setUp(self):
        super(ReviewDealerRaterTest, self).setUp()
        self.flask_set_up()
        self.app.register_blueprint(api, url_prefix=self.API_VERSION)

        cache.init_app(self.app, config={'CACHE_TYPE': 'simple'})

        # TODO: patch to mock celery call workflow
        # self.dealerrater_workflow_patch = patch(
        #     'barsky_scrapper.services.dealer_rater_service.reviews.routes.dealerrater_workflow.delay')
        # self.dealerrater_workflow = self.dealerrater_workflow_patch.start()
        
        self.env = dict(
            API_DEALER_RATER='http://api.dealerrater',
            DEALER_RATER_BUICK='buickendpoint',
        )

        self.dealerrater_config_patch = patch(
            'barsky_scrapper.services.dealer_rater_service.get_config')
        self.dealerrater_config = self.dealerrater_config_patch.start()
        self.dealerrater_config.return_value = {
            k.lower(): v for k, v in self.env.items()}

        self.bucket_set_up()
        self.dealerraterservice_set_up()

    def tearDown(self):
        super(ReviewDealerRaterTest, self).tearDown()
        # self.dealerrater_workflow_patch.stop()
        self.dealerrater_config_patch.stop()
        self.dealerraterservice_tear_down()
        self.datetime_tear_down()

    @property
    def headers(self):
        headers = {}

        # INFO: ready for api authentication
        if hasattr(self, 'access_token'):
            headers['Authorization'] = f'Bearer {self.access_token}'

        headers['Content-Type'] = 'application/json'

        return headers

    def assert_response_review_has(self, field, index=0):
        data = self.response.json
        data = data[0]['reviews'][index]
        
        breadcrumb = field.split('__')
        
        if len(breadcrumb) == 1:
            self.assertIn(field, data)
            self.assertIsNotNone(data[field])
        else:
            raise NotImplementedError()

    def given_pages_to_be_scraped(self, num):
        self._page = num

    def when_retrieve_the_reviews(self):
        self.response = self.client.get(
            f'/v1/reviews/buick/{self._page}', headers=self.headers)

    def when_retrieve_the_suspicious(self):
        self.response = self.client.get(
            f'/v1/reviews/buick/suspicious', headers=self.headers)

    def assert_dealerrater_workflow_get_called(self):
        self.assertTrue(self.dealerrater_workflow.called)

    def assert_return_is(self, expected_type):
        self.assertEqual(type(self.response.json), expected_type)

    def assert_response_reviews_has(self, field):
        self.assertIn(field, self.response.json)

    def assert_response_reviews_count(self, field, count):
        self.assertEqual(len(self.response.json[field]), count)

