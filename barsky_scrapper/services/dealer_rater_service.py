from barsky_scrapper.helper import get_config
from barsky_scrapper.services.mixins import HttpMixin


__all__ = ['DealerRaterService']


class DealerRaterService:
    REVIEW = '{api}/{endpoint}/page{page_num}'

    def __init__(self):
        self._dealer_rater_api = get_config().get('api_dealer_rater')
        self._buick_endpoint = get_config().get('dealer_rater_buick')
        self._http = HttpMixin()

    def buick(self, page=1):
        result = self._http.get(
            self.REVIEW.format(
                api=self._dealer_rater_api, 
                endpoint=self._buick_endpoint, 
                page_num=page
            )
        )

        return { 'html': result.text, 'status': result.status_code, 'page': page }
