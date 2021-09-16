from datetime import datetime
from unittest import skip


class ReviewDealerRaterAPISpec:

    def given_pages_to_be_scraped(self, num):
        raise NotImplementedError()

    def given_cache(self, key, value):
        raise NotImplementedError()

    def given_today_is(self, year, month, day):
        raise NotImplementedError()

    def given_file_in_bucket(self, file_name):
        raise NotImplementedError()

    def given_dealer_rater_entry_with(self, **kwargs):
        raise NotImplementedError()

    def given_file_not_on_bucket(self, filename):
        raise NotImplementedError()

    def when_retrieve_the_reviews(self):
        raise NotImplementedError()

    def assert_accecpted(self):
        raise NotImplementedError()

    def assert_not_modified(self):
        raise NotImplementedError()

    def assert_dealerrater_workflow_get_called(self):
        raise NotImplementedError()

    def assert_response_has(self, index=None, status_code=[200, 201, 202, 304], **kwargs):
        raise NotImplementedError()

    def assert_response_is(self, status_code, expected):
        raise NotImplementedError()

    def assert_response_not_none(self, field, index=0):
        raise NotImplementedError()

    def assert_response_count(self, count, status_code=200):
        raise NotImplementedError()

    def assert_response_review_has(self, field, index=0):
        raise NotImplementedError()

    def assert_ok(self):
        raise NotImplementedError()

    def assert_accecpted(self):
        raise NotImplementedError()

    def test_01_route_is_available(self):
        self.given_pages_to_be_scraped(5)
        self.when_retrieve_the_reviews()
        self.assert_ok()
    
    def test_02_list_of_reviews_count_match_page_requested(self):
        self.given_pages_to_be_scraped(2)
        self.when_retrieve_the_reviews()
        self.assert_response_count(2)
    
    def test_03_list_of_reviews_count_match_page_requested_when_nothing_was_sent(self):
        self.given_pages_to_be_scraped(0)
        self.when_retrieve_the_reviews()
        self.assert_response_count(1)

    def test_04_has_not_empty_reviews(self):
        self.given_pages_to_be_scraped(1)
        self.when_retrieve_the_reviews()
        self.assert_response_not_none(field='reviews')

    def test_05_has_not_empty_review_page(self):
        self.given_pages_to_be_scraped(1)
        self.when_retrieve_the_reviews()
        self.assert_response_not_none(field='page')

    def test_06_reviews_returned_has_title(self):
        self.given_pages_to_be_scraped(1)
        self.when_retrieve_the_reviews()
        self.assert_response_review_has(field='title')
    
    def test_07_reviews_returned_has_text(self):
        self.given_pages_to_be_scraped(1)
        self.when_retrieve_the_reviews()
        self.assert_response_review_has(field='text')
    
    def test_08_reviews_returned_has_date(self):
        self.given_pages_to_be_scraped(1)
        self.when_retrieve_the_reviews()
        self.assert_response_review_has(field='date')
    
    def test_08_reviews_returned_has_user(self):
        self.given_pages_to_be_scraped(1)
        self.when_retrieve_the_reviews()
        self.assert_response_review_has(field='user')
    
    def test_09_reviews_returned_has_fakeLevelLabel(self):
        self.given_pages_to_be_scraped(1)
        self.when_retrieve_the_reviews()
        self.assert_response_review_has(field='fakeLevelLabel')
    
    def test_10_reviews_returned_has_fakeLevelvalue(self):
        self.given_pages_to_be_scraped(1)
        self.when_retrieve_the_reviews()
        self.assert_response_review_has(field='fakeLevelValue')
    
    def test_11_reviews_returned_has_ratings(self):
        self.given_pages_to_be_scraped(1)
        self.when_retrieve_the_reviews()
        self.assert_response_review_has(field='ratings')
    
    def test_12_reviews_returned_employees(self):
        self.given_pages_to_be_scraped(1)
        self.when_retrieve_the_reviews()
        self.assert_response_review_has(field='employees')
    

    @skip('workflow with celery aim capability of parallelism')
    def test_01_scrapping_started_async_process(self):
        self.when_retrieve_the_reviews()
        self.assert_accecpted()

    @skip('workflow with celery aim capability of parallelism')
    def test_02_scrapping_started_async_process_retrieve_status_and_message(self):
        self.when_retrieve_the_reviews()
        self.assert_accecpted()
        self.assert_response_has(status='Accecpted', message='Triggered the scraper')

    @skip('workflow with celery aim capability of parallelism')
    def test_03_scrapping_workflow_get_call(self):
        self.when_retrieve_the_reviews()
        self.assert_dealerrater_workflow_get_called()
    
    @skip('workflow with celery aim capability of parallelism')
    def test_04_scrapping_workflow_cache_pending_retrive_status_and_message(self):
        reference = datetime.now().strftime('%Y-%m-%d')
        self.given_cache(f'{reference}-pending', 'pending')
        self.when_retrieve_the_reviews()
        self.assert_not_modified()

    @skip('workflow with celery aim capability of parallelism')
    def test_05_scrapping_workflow_accecpted_the_task_and_started_scrapping(self):
        self.given_today_is('2021','09','22')
        self.given_file_not_on_bucket('dealer_rater_2021-09-22.json')
        self.given_dealer_rater_entry_with(
            title='"Raymond Prazak was very patient & helpful! He worked hard..." - Jenna Cowling',
            body="""Raymond Prazak was very patient & helpful! He worked hard to find the 
            best vehicle to fit our budget! No pressure to buy the most expensive one! 😁""",
            raiting__customer_service=5,
            raiting__quality_of_work=5,
            raiting__friendliness=5,
            raiting__pricing=5,
            raiting__overrall_experience=5,
            raiting__recommend_dealer=True,
        )

        self.when_retrieve_the_reviews()
        self.assert_accecpted()

    @skip('workflow with celery aim capability of parallelism')
    def test_06_scrapping_workflow_mapper(self):
        self.given_today_is('2021','09','22')
        self.given_file_in_bucket('dealer_rater_2021-09-22.json')
        self.given_dealer_rater_entry_with(
            title='"Raymond Prazak was very patient & helpful! He worked hard..." - Jenna Cowling',
            body="""Raymond Prazak was very patient & helpful! He worked hard to find the 
            best vehicle to fit our budget! No pressure to buy the most expensive one! 😁""",
            raiting__customer_service=5,
            raiting__quality_of_work=5,
            raiting__friendliness=5,
            raiting__pricing=5,
            raiting__overrall_experience=5,
            raiting__recommend_dealer=True,
        )

        self.when_retrieve_the_rating()
        self.assert_ok()

        self.assert_response_is(200, {
            'dealer_rater_reviews': [{
                'id': 'someuuid',
                'title': '"Raymond Prazak was very patient & helpful! He worked hard..." - Jenna Cowling',
                'text': 'Raymond Prazak was very patient & helpful! He worked hard to find the best vehicle to fit our budget! No pressure to buy the most expensive one! 😁',
                'raitings': {
                    'customer_service': 5,
                    'quality_of_work': 5,
                    'friendliness': 5,
                    'pricing': 5,
                    'overrall_experience': 5,
                    'recommend_dealer': 5
                }
            }]
        })