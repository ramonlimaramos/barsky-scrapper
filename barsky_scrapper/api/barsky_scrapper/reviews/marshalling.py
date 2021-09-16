from flask_restx import fields
from barsky_scrapper.api.barsky_scrapper.reviews.definition import ns


__all__ = ['dealer_rater_response', 'in_progress_response']


raitings = ns.model('raitings', {
    'dealRating': fields.Float,
    'customerService': fields.Float,
    'friendliness': fields.Float,
    'pricing': fields.Float,
    'overrallExperience': fields.Float,
    'recommendDealer': fields.Boolean,
})


employees = ns.model('employee', {
    'name': fields.String,
    'raiting' : fields.Integer,
})


review = ns.model('review', {
    'title': fields.String,
    'text': fields.String,
    'date': fields.String,
    'user': fields.String,
    'raitings': fields.Nested(raitings),
    'employees': fields.Nested(employees),
})

review_suspicious = ns.model('review', {
    'title': fields.String,
    'text': fields.String,
    'date': fields.String,
    'user': fields.String,
    'fakeLevelLabel': fields.String,
    'fakeLevelValue': fields.String,
    'raitings': fields.Nested(raitings),
    'employees': fields.Nested(employees),
})


dealer_rater_response = ns.model('dealer_rater_response', {
    'reviews': fields.List(fields.Nested(review)),
    'page': fields.Integer,
})


dealer_rater_suspicious_response = ns.model('dealer_rater_suspicious', {
    'reviews': fields.List(fields.Nested(review_suspicious))
})


in_progress_response = ns.model('processing_data', {
    'status': fields.String,
    'message': fields.String,
})