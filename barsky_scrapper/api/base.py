from flask import Blueprint, current_app, url_for
from flask_restx import Api

__all__ = ['api', 'swagger_doc']


class CustomAPI(Api):
    @property
    def specs_url(self):
        """
        The Swagger specifications absolute url (ie. `swagger.json`)
        :rtype: str
        """
        return url_for(self.endpoint("specs"), _external=True,
                       _scheme=current_app.config.get('PREFERRED_URL_SCHEME'))


swagger_doc = Blueprint('swagger_doc_redirection', __name__)
api = Blueprint('coreography_api', __name__)