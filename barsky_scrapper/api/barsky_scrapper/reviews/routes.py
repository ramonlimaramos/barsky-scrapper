from flask_restx import Resource

from barsky_scrapper.api.barsky_scrapper.reviews.definition import ns
from barsky_scrapper.api.barsky_scrapper.reviews.marshalling import (
    dealer_rater_response, dealer_rater_suspicious_response, in_progress_response)

from barsky_scrapper.services import DealerRaterService
from barsky_scrapper.domain import AdapterBuickReview

# TODO: workflow with celery aim capability of parallelism
# from barsky_scrapper.services import dealerrater_workflow
# from barsky_scrapper.helper import get_bucket
# from barsky_scrapper.cache import cache


@ns.doc('Raiting resource swagger doc')
@ns.route('/buick/<maxpages>')
class DealerRaterBuickController(Resource):

    @ns.doc('Get all reviews from the dealerrater.com for McKaig Chevrolet Buick')
    @ns.response(200, 'Successful executed', model=dealer_rater_response)

    # TODO: workflow with celery aim capability of parallelism
    # @ns.response(202, 'Accecpted and triggered', model=in_progress_response)
    # @ns.response(304, 'Scrapping is processing', model=in_progress_response)
    def get(self, maxpages):
        maxpages = int(maxpages) if int(maxpages) > 0 else 1
        dealer_rater_service = DealerRaterService()
        reviews = AdapterBuickReview(service=dealer_rater_service, total=int(maxpages))

        return reviews.all, 200

        # TODO: workflow with celery aim capability of parallelism
        # reference = datetime.now().strftime('%Y-%m-%d')
        # reference_scrapped_result = f'dealer_rater_{reference}.json'
        # bucket = get_bucket()

        # if cache.get(f'{reference}-pending'):
        #     return {'status': 'Not Modified', 'message': 'Processing'}, 304

        # if bucket.exists(reference_scrapped_result):
        #     return reference_scrapped_result, 200

        # else:
        #     dealerrater_workflow.delay()
        #     return {'status': 'Accecpted', 'message': 'Triggered the scraper'}, 202


@ns.route('/buick/suspicious')
class DealerRaterBuickController(Resource):

    @ns.doc('Get top 3 reviews suspicious from the dealerrater.com for McKaig Chevrolet Buick')
    @ns.response(200, 'Successful executed', model=dealer_rater_suspicious_response)
    # TODO: workflow with celery aim capability of parallelism
    # @ns.response(202, 'Accecpted and triggered', model=in_progress_response)
    # @ns.response(304, 'Scrapping is processing', model=in_progress_response)

    @ns.doc('Get top 3 reviews suspicious from the dealerrater.com for McKaig Chevrolet Buick')
    @ns.response(200, 'Successful executed', model=dealer_rater_suspicious_response)
    def get(self):
        dealer_rater_service = DealerRaterService()
        reviews = AdapterBuickReview(service=dealer_rater_service)

        return reviews.most_suspicious, 200

        # TODO: workflow with celery aim capability of parallelism
        # reference = datetime.now().strftime('%Y-%m-%d')
        # reference_scrapped_result = f'dealer_rater_{reference}.json'
        # bucket = get_bucket()

        # if cache.get(f'{reference}-pending'):
        #     return {'status': 'Not Modified', 'message': 'Processing'}, 304

        # if bucket.exists(reference_scrapped_result):
        #     return reference_scrapped_result, 200

        # else:
        #     dealerrater_workflow.delay()
        #     return {'status': 'Accecpted', 'message': 'Triggered the scraper'}, 202
