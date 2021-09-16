import os
import json
import re
import httpretty
import json

from datetime import datetime
from random import randint
from bs4 import BeautifulSoup


__all__ = ['DealerRaterServiceMixin']


here = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(here, '..', 'fixtures', 'dealerrater_fixture.html'), 'r') as f:
    dealer_rater_fixture = f.read()


class DealerRaterMixin:

    def dealer_rater_set_up(self):
        self.dealer_rater_template = dealer_rater_fixture

    def dealer_rater_tear_down(self):
        pass

    def __review_container_entry(self, date, title, body, raitings):
        return f"""
            <div class="review-entry col-xs-12 text-left pad-none pad-top-lg  border-bottom-teal-lt">
            {date} 
            {title}
            {body}
            {raitings}
            </div>
        """
    
    def __review_date_entry(self, full_rate_int):
        now = datetime.now()
        date = now.strftime('%d %B, %Y')
        return f"""
            <div class="col-xs-12 col-sm-3 pad-left-none text-center review-date margin-bottom-md">
                <div class="italic col-xs-6 col-sm-12 pad-none margin-none font-20">{date}</div>
                <div class="col-xs-6 col-sm-12 pad-none dealership-rating">
                    <div class="rating-static visible-xs pad-none margin-none rating-{full_rate_int}0 pull-right"></div>
                    <div class="rating-static hidden-xs rating-50 margin-center"></div>
                    <div class="col-xs-12 hidden-xs pad-none margin-top-sm small-text dr-grey">SALES VISIT - NEW</div>
                </div>
            </div>
        """
    
    def __review_title(self, title_str):
        user = title_str.split(' - ')
        return f"""
            <div class="col-xs-12 col-sm-9 pad-none review-wrapper">
                <div class="margin-bottom-sm line-height-150">
                    <h3 class="no-format inline italic-bolder font-20 dark-grey">{user[0]}</h3>
                    <span class="italic font-18 black notranslate">- {user[1]}</span>
                </div>
            </div>
        """
    
    def __review_body(self, body_str):
        rand_of_six_digits = randint(10**(6-1), (10**6)-1)
        return f"""
            <div class="tr margin-top-md">
                <div class="td text-left valign-top ">
                    <p class="font-16 review-content margin-bottom-none line-height-25">
                    {body_str}
                    </p>
                    <a id="{rand_of_six_digits}" class="read-more-toggle pointer line-height-25 small-text block margin-bottom-md">Read More</a>
                </div>
            </div>
        """
    
    def __review_raitings(self, **kwargs):
        recommend_it = 'Yes' if kwargs['recommend_dealer'] == True else 'No'
        return f"""
        <div class="pull-left pad-left-md pad-right-md bg-grey-lt margin-bottom-md review-ratings-all review-hide">
            <!-- REVIEW RATING - CUSTOMER SERVICE -->
            <div class="table width-100 pad-left-none pad-right-none margin-bottom-md">
                <div class="tr">
                    <div class="lt-grey small-text td">Customer Service</div>
                    <div class="rating-static-indv rating-{kwargs['customer_service']}0 margin-top-none td"></div>
                </div>
                <!-- REVIEW RATING - QUALITY OF WORK -->
                <div class="tr margin-bottom-md">
                    <div class="lt-grey small-text td">Quality of Work</div>
                    <div class="rating-static-indv rating-{kwargs['quality_of_work']}0 margin-top-none td"></div>
                </div>
                <!-- REVIEW RATING - FRIENDLINESS -->
                <div class="tr margin-bottom-md">
                    <div class="lt-grey small-text td">Friendliness</div>
                    <div class="rating-static-indv rating-{kwargs['friendliness']}0 margin-top-none td"></div>
                </div>
                <!-- REVIEW RATING - PRICING -->
                <div class="tr margin-bottom-md">
                    <div class="lt-grey small-text td">Pricing</div>
                    <div class="rating-static-indv rating-{kwargs['pricing']}0 margin-top-none td"></div>
                </div>
                <!-- REVIEW RATING - EXPERIENCE -->
                <div class="tr margin-bottom-md">
                    <div class="td lt-grey small-text">Overall Experience</div>
                    <div class="rating-static-indv rating-{kwargs['overrall_experience']}0 margin-top-none td"></div>
                </div>
                <!-- REVIEW RATING - RECOMMEND DEALER -->
                <div class="tr">
                    <div class="lt-grey small-text td">Recommend Dealer</div>
                    <div class="td small-text boldest">
                        {recommend_it}
                    </div>
                </div>
            </div>
        </div>
        """

    def append_entry_to_fixture(self, **kwargs):
        soup = BeautifulSoup(self.dealer_rater_template, 'html.parser')

        raitings_section = {k.split('raiting__')[1]: v for k, v in kwargs.items() if k.startswith('raiting')}
        entry = self.__review_container_entry(
            self.__review_date_entry(5),
            self.__review_title(kwargs['title']),
            self.__review_body(kwargs['body']),
            self.__review_raitings(**raitings_section)
        )

        soup.find('div', {'class': 'review-entry'})\
            .append(BeautifulSoup(entry, 'html.parser'))

        return soup


class DealerRaterServiceMixin(DealerRaterMixin):
    endpoint = 'buickendpoint'
    dealerraterservice_regex = r'http://api\.dealerrater/'+endpoint+'/page(?P<page_num>[\d\-\w]+)'

    def dealerraterservice_set_up(self):
        self.dealer_rater_set_up()
        self.dealer_rater_result = self.dealer_rater_template
        self.dealerraterservice_get_call = False
        self.dealerraterservice_status = False
        self.dealerraterservice_message = False

        if not httpretty.is_enabled():
            httpretty.enable()

        httpretty.register_uri(httpretty.GET,
                               re.compile(self.dealerraterservice_regex),
                               body=self.get_dealerrater_callback)

    def dealerraterservice_tear_down(self):
        self.dealer_rater_tear_down()

        if httpretty.is_enabled():
            httpretty.disable()
            httpretty.reset()

    def given_dealer_rater_entry_with(self, **kwargs):
        allowed_keys = (
            'title', 'body', 'raiting__customer_service', 'raiting__quality_of_work', 
            'raiting__friendliness', 'raiting__pricing', 
            'raiting__overrall_experience', 'raiting__recommend_dealer'
        )

        is_allowed_keys = any(x in allowed_keys for x in kwargs.keys())
        if is_allowed_keys:
            self.dealer_rater_result = self.append_entry_to_fixture(**kwargs)

    def get_dealerrater_callback(self, request, uri, headers):
        self.request = request
        m = re.match(self.dealerraterservice_regex, uri)
        if m:
            return [200, {'content-type': 'text/html'}, self.dealer_rater_result]
        return [400, {'content-type': 'text/html'}, 'Bad Request']