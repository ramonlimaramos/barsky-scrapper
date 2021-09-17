import re

from bs4 import BeautifulSoup

from abc import ABCMeta, abstractclassmethod, abstractmethod

from barsky_scrapper.domain import Review, Employee, Ratings, ScoreAnalyzer
from barsky_scrapper.helper import remove_escapes, bubble_sort


__all__ = ['BuilderBuick', 'AdapterBuickReview']


class TemplateBuilder:

    __metaclass__ = ABCMeta

    @abstractclassmethod
    def build(cls, soup):
        pass


class TemplateAdapter:

    __metaclass__ = ABCMeta

    def __init__(self, service, **kwargs):
        pass

    @abstractmethod
    def transform(self):
        pass



class BuilderBuick(TemplateBuilder):

    @classmethod
    def build(cls, soup):
        elements = soup.find_all('div', class_='review-entry')

        return [dict(
            Review(
                title=cls._get_title(x),
                text=cls._get_text(x),
                date=cls._get_date(x),
                user=cls._get_user(x),
                fake_level_label=ScoreAnalyzer(
                    cls._get_text(x), cls._get_ratings(x)).label,
                fake_level_value=ScoreAnalyzer(
                    cls._get_text(x), cls._get_ratings(x)).value,
                ratings=cls._get_ratings(x),
                employees=cls._get_employees(x),
            )) for x in elements]

    @classmethod
    def _get_title(cls, html, **kwargs):
        title = None
        if html.find('h3'):
            title = html.find('h3').text
        return remove_escapes(title.replace('\"', '')) if title is not None else ''

    @classmethod
    def _get_text(cls, html):
        text = None
        if len(html.select('.review-content')) > 0:
            text = str(html.select('.review-content')[0].text)
        return remove_escapes(text.strip()) if text is not None else ''

    @classmethod
    def _get_date(cls, html):
        date = None
        if len(html.select('.review-date > :first-child')) > 0:
            date = str(html.select('.review-date > :first-child')[0].text)
        return remove_escapes(date) if date is not None else ''

    @classmethod
    def _get_user(cls, html):
        user = None
        if len(html.select('.review-wrapper > :first-child')) > 0:
            user = str(
                html.select('.review-wrapper > :first-child')[0]
                .span.text.replace('- ', '')
            )
        return remove_escapes(user) if user is not None else ''

    @classmethod
    def _get_ratings(cls, html):
        def build_deal_rating():
            element = html.select(
                '.dealership-rating > :first-child')[0]['class']
            dealrating = re.sub('\D', '', ''.join(element))
            if dealrating:
                return float(dealrating)
            return ''

        def build_ratings(elements, key):
            found_element = [x for x in elements if key in x]
            if len(found_element) == 1:
                indexcontent = elements.index(found_element[0]) + 1
            else:
                return ''

            if key == 'Recommend Dealer':
                rating = elements[indexcontent].text
                return (True, False)[rating == 'Yes']
            else:
                rating = re.sub('\D', '', ''.join(
                    elements[indexcontent]['class']))
                return float(rating) if rating else ''

        r = html.select('.review-ratings-all>div.table>div.tr>div.td')
        if len(r) == 0:
            return {}

        ratings = Ratings(
            customer_service=build_ratings(r, 'Customer Service'),
            friendliness=build_ratings(r, 'Friendliness'),
            pricing=build_ratings(r, 'Pricing'),
            overrall_experience=build_ratings(r, 'Overall Experience'),
            recommend_dealer=build_ratings(r, 'Recommend Dealer'),
        )
        ratings.set_deal(build_deal_rating())

        return dict(ratings)

    @classmethod
    def _get_employees(cls, html):
        def build_name(e):
            return ('', str(e.find('a').text).strip().replace('\"', ''))[e.find('a').text is not None]

        def build_raiting(e):
            return (0, float(e.find('span').text))[e.find('span').text is not None]

        return [
            dict(Employee(name=build_name(e), raiting=build_raiting(e)))
            for e in html.select('.review-employee')
        ]

    def __repr__(self):
        return f'<BuilderBuick>'


class AdapterBuickReview(TemplateAdapter):

    def __init__(self, service, **kwargs):
        self._service = service
        self._max_len = kwargs.get('total', 5)
        self.transform()

    def transform(self):
        self._list_review = list(
            map(
                lambda y: {
                    'reviews': BuilderBuick.build(BeautifulSoup(y['html'], 'html.parser')),
                    'page': y['page']
                },
                filter(lambda i: i['status'] == 200,
                       [self._service.buick(page=x)
                        for x in range(1, (self._max_len + 1))]
                       )
            )
        )

    @property
    def all(self):
        return self._list_review

    @property
    def most_suspicious(self):
        flat = [review for items in self._list_review for review in items['reviews']]
        to_sort = [(items, items['fakeLevelValue']) for items in flat]
        most_suspicious = [item[0] for item in bubble_sort(to_sort)]
        return {'reviews': most_suspicious[:3]}
