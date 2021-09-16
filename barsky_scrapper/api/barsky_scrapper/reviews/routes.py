from flask_restx import Resource

from barsky_scrapper.api.barsky_scrapper.reviews.definition import ns
from barsky_scrapper.api.barsky_scrapper.reviews.marshalling import (
    dealer_rater_response, dealer_rater_suspicious_response, in_progress_response)

from barsky_scrapper.services import DealerRaterService
from barsky_scrapper.domain import AdapterBuickReview



@ns.doc('Raiting resource swagger doc')
@ns.route('/buick/<maxpages>')
class DealerRaterBuickController(Resource):

    @ns.doc('Get all reviews from the dealerrater.com for McKaig Chevrolet Buick')
    @ns.response(200, 'Successful executed', model=dealer_rater_response)

    def get(self, maxpages):
        return reviews.all, 200
@ns.route('/buick/suspicious')
class DealerRaterBuickController(Resource):

    @ns.doc('Get top 3 reviews suspicious from the dealerrater.com for McKaig Chevrolet Buick')
    @ns.response(200, 'Successful executed', model=dealer_rater_suspicious_response)
    def get(self, maxpages):
        return reviews.all, 200
