from barsky_scrapper.helper import to_camel_case


__all__ = ['Ratings']


class Ratings:

    def __init__(self, customer_service, friendliness, pricing,
                 overrall_experience, recommend_dealer):
        self._deal_rating = ''
        self._customer_service = customer_service
        self._friendliness = friendliness
        self._pricing = pricing
        self._overrall_experience = overrall_experience
        self._recommend_dealer = recommend_dealer

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield(to_camel_case(attr[1:]), value)

    def set_deal(self, deal_val):
        self._deal_rating = deal_val

    def __repr__(self):
        return f'<Ratings {self._pricing}>'