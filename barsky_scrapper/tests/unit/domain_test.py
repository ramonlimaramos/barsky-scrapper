from unittest import TestCase

from barsky_scrapper.tests.domain_spec import AdapterBuilderSpec, AnalyzerSpec
from barsky_scrapper.domain import AdapterBuickReview, ScoreAnalyzer


class AnalyzerTest(AnalyzerSpec, TestCase):

    def setUp(self):
        super(AnalyzerTest, self).setUp()

    def tearDown(self):
        super(AnalyzerTest, self).tearDown()

    def given_text_is(self, text):
        self._text = text

    def when_executes_buick_score(self):
        self._response_count = ScoreAnalyzer(self._text)

    def assert_score_value(self, count):
        self.assertEqual(count, self._response_count.value)


class AdapterBuilderTest(AdapterBuilderSpec, TestCase):

    def setUp(self):
        super(AdapterBuilderTest, self).setUp()
        self._html = ''

        class FakeService:
            @classmethod
            def buick(cls, page=0, **kwargs):
                return {'html': self._html, 'status': 200, 'page': page}

        self._fake_service = FakeService

    def tearDown(self):
        super(AdapterBuilderTest, self).tearDown()

    def given_html_is(self, html):
        self._html = html

    def when_executes_buick_builder(self):
        self._response = AdapterBuickReview(self._fake_service, total=1)

    def assert_transformed_to(self, expected):
        self.assertEqual(expected, self._response.all)