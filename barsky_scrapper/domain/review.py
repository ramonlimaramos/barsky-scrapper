import uuid
from barsky_scrapper.helper import to_camel_case


__all__ = ['Review']


class Review:

    def __init__(self, title, text, date,
    user, fake_level_label, fake_level_value, 
    ratings, employees):
        self._uuid = uuid.uuid4()
        self._title = title
        self._text = text
        self._date = date
        self._user = user
        self._fake_level_label = fake_level_label
        self._fake_level_value = fake_level_value
        self._ratings = ratings
        self._employees = employees

    def __iter__(self):
        for attr, value in self.__dict__.items():
            value = value.hex if isinstance(value, uuid.UUID) else value
            yield(to_camel_case(attr[1:]), value)

    def __repr__(self):
        return f'<Review {self._title[:5]}...>'
