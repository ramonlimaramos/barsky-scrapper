

class AnalyzerSpec:

    def given_text_is(self, text):
        raise NotImplementedError()

    def when_executes_buick_score(self):
        raise NotImplementedError()

    def assert_score_value(self, count):
        raise NotImplementedError()
    
    def test_01_analyzer_empty(self):
        self.given_text_is('')
        self.when_executes_buick_score()
        self.assert_score_value(0)


class AdapterBuilderSpec:

    def given_html_is(self, html):
        raise NotImplementedError()

    def when_executes_buick_builder(self):
        raise NotImplementedError()

    def assert_transformed_to(self, expected):
        raise NotImplementedError()

    def test_01_adapter_builder_transform_empty(self):
        self.given_html_is('')
        self.when_executes_buick_builder()
        self.assert_transformed_to([{'page': 1, 'reviews': []}])
    
    def test_02_adapter_builder_transform_entry_title_review(self):
        self.given_html_is("""
        <div class="review-entry col-xs-12 text-left pad-none pad-top-lg  border-bottom-teal-lt">
            <h3 class="no-format inline italic-bolder font-20 dark-grey">Here is the title</h3>
        </div>
        """)
        self.when_executes_buick_builder()
        self.assert_transformed_to(
            [{
                'page': 1,
                'reviews': [{
                    'date': '',
                    'employees': [],
                    'fakeLevelLabel': '',
                    'fakeLevelValue': 0,
                    'ratings': {},
                    'text': '',
                    'title': 'Here is the title',
                    'user': ''
                }],
            }]
        )
    
    def test_03_adapter_builder_transform_entry_date_review(self):
        self.given_html_is("""
        <div class="review-entry col-xs-12 text-left pad-none pad-top-lg  border-bottom-teal-lt">
            <div class="col-xs-12 col-sm-3 pad-left-none text-center review-date margin-bottom-md">
                <div class="italic col-xs-6 col-sm-12 pad-none margin-none font-20">September 15, 2021</div>
                <div class="col-xs-6 col-sm-12 pad-none dealership-rating">
                    <div class="rating-static visible-xs pad-none margin-none rating-50 pull-right"></div>
                    <div class="rating-static hidden-xs rating-50 margin-center"></div>
                    <div class="col-xs-12 hidden-xs pad-none margin-top-sm small-text dr-grey">SALES VISIT - NEW</div>
                </div>
            </div>
        </div>
        """)
        self.when_executes_buick_builder()
        self.assert_transformed_to(
            [{
                'page': 1,
                'reviews': [{
                    'date': 'September 15, 2021',
                    'employees': [],
                    'fakeLevelLabel': '',
                    'fakeLevelValue': 0,
                    'ratings': {},
                    'text': '',
                    'title': '',
                    'user': ''
                }],
            }]
        )
    
    def test_04_adapter_builder_transform_entry_text_review(self):
        self.given_html_is("""
        <div class="review-entry col-xs-12 text-left pad-none pad-top-lg  border-bottom-teal-lt">
            <div class="tr margin-top-md">
                <div class="td text-left valign-top ">
                    <p class="font-16 review-content margin-bottom-none line-height-25">
                    Python every where people
                    </p>
                </div>
            </div>
        </div>
        """)
        self.when_executes_buick_builder()
        self.assert_transformed_to(
            [{
                'page': 1,
                'reviews': [{
                    'date': '',
                    'employees': [],
                    'fakeLevelLabel': '',
                    'fakeLevelValue': 0,
                    'ratings': {},
                    'text': 'Python every where people',
                    'title': '',
                    'user': ''
                }],
            }]
        )
    
    def test_05_adapter_builder_transform_entry_user_review(self):
        self.given_html_is("""
        <div class="review-entry col-xs-12 text-left pad-none pad-top-lg  border-bottom-teal-lt">
            <div class="col-xs-12 col-sm-9 pad-none review-wrapper">
                <div class="margin-bottom-sm line-height-150">
                    <h3 class="no-format inline italic-bolder font-20 dark-grey"></h3>
                    <span class="italic font-18 black notranslate">- ramonlimaramos</span>
                </div>
            </div>
        </div>
        """)
        self.when_executes_buick_builder()
        self.assert_transformed_to(
            [{
                'page': 1,
                'reviews': [{
                    'date': '',
                    'employees': [],
                    'fakeLevelLabel': '',
                    'fakeLevelValue': 0,
                    'ratings': {},
                    'text': '',
                    'title': '',
                    'user': 'ramonlimaramos'
                }],
            }]
        )
    
    def test_06_adapter_builder_transform_entry_employees_review(self):
        self.given_html_is("""
        <div class="review-entry col-xs-12 text-left pad-none pad-top-lg  border-bottom-teal-lt">
            <div class="clear-fix  margin-top-sm">
                <div class="col-xs-12 lt-grey pad-left-none employees-wrapper">
                    <div class="small-text">Employees Worked With </div>
                    <div class="col-xs-12 col-sm-6 col-md-4 pad-left-none pad-top-sm pad-bottom-sm review-employee">
                        <div class="table">
                            <div class="td square-image employee-image" style="background-image: url(https://cdn-user.dealerrater.com/images/dealer/23685/employees/ca22768af3f7.jpg)"></div>
                            <div class="td valign-bottom pad-left-md pad-top-none pad-bottom-none">
                                <a class="notranslate pull-left line-height-1 tagged-emp small-text teal  margin-right-sm emp-640356" data-emp-id="640356" href="/sales/Taylor-Prickett-review-640356/">
                                                        Taylor Prickett
                                                    </a>
                                <div class="col-xs-12 pad-none margin-none pad-top-sm">
                                    <div class="relative employee-rating-badge-sm">
                                        <div class="col-xs-12 pad-none">
                                            <span class="pull-left font-14 boldest lt-grey line-height-1 pad-right-sm margin-right-sm border-right">5.0</span>
                                            <div class="rating-static rating-50 margin-top-none pull-left"></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-xs-12 col-sm-6 col-md-4 pad-left-none pad-top-sm pad-bottom-sm review-employee">
                        <div class="table">
                            <div class="td square-image employee-image" style="background-image: url(https://cdn-user.dealerrater.com/images/dealer/23685/employees/307448fc2105.jpg)"></div>
                            <div class="td valign-bottom pad-left-md pad-top-none pad-bottom-none">
                                <a class="notranslate pull-left line-height-1 tagged-emp small-text teal   emp-507162" data-emp-id="507162" href="/sales/Dennis-Smith-review-507162/">
                                                        Dennis Smith
                                                    </a>
                                <div class="col-xs-12 pad-none margin-none pad-top-sm">
                                    <div class="relative employee-rating-badge-sm">
                                        <div class="col-xs-12 pad-none">
                                            <span class="pull-left font-14 boldest lt-grey line-height-1 pad-right-sm margin-right-sm border-right">5.0</span>
                                            <div class="rating-static rating-50 margin-top-none pull-left"></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """)
        self.when_executes_buick_builder()
        self.assert_transformed_to(
            [{
                'page': 1,
                'reviews': [{
                    'date': '',
                    'employees': [
                        {'name': 'Taylor Prickett', 'rating': 5.0 }, 
                        { 'name': 'Dennis Smith', 'rating': 5.0 }
                    ],
                    'fakeLevelLabel': '',
                    'fakeLevelValue': 0,
                    'ratings': {},
                    'text': '',
                    'title': '',
                    'user': ''
                }],
            }]
        )

    def test_07_adapter_builder_transform_entry_ratings_review(self):
        self.given_html_is("""
        <div class="review-entry col-xs-12 text-left pad-none pad-top-lg  border-bottom-teal-lt">
            <div class="col-xs-12 col-sm-3 pad-left-none text-center review-date margin-bottom-md">
                <div class="italic col-xs-6 col-sm-12 pad-none margin-none font-20"></div>
                <div class="col-xs-6 col-sm-12 pad-none dealership-rating">
                    <div class="rating-static visible-xs pad-none margin-none rating-50 pull-right"></div>
                    <div class="rating-static hidden-xs rating-50 margin-center"></div>
                    <div class="col-xs-12 hidden-xs pad-none margin-top-sm small-text dr-grey">SALES VISIT - NEW</div>
                </div>
            </div>

            <div class="pull-left pad-left-md pad-right-md bg-grey-lt margin-bottom-md review-ratings-all review-hide">
                <!-- REVIEW RATING - CUSTOMER SERVICE -->
                <div class="table width-100 pad-left-none pad-right-none margin-bottom-md">
                    <div class="tr">
                        <div class="lt-grey small-text td">Customer Service</div>
                        <div class="rating-static-indv rating-50 margin-top-none td"></div>
                    </div>
                    <!-- REVIEW RATING - QUALITY OF WORK -->
                    <div class="tr margin-bottom-md">
                        <div class="lt-grey small-text td">Quality of Work</div>
                        <div class="rating-static-indv rating-00 margin-top-none td"></div>
                    </div>
                    <!-- REVIEW RATING - FRIENDLINESS -->
                    <div class="tr margin-bottom-md">
                        <div class="lt-grey small-text td">Friendliness</div>
                        <div class="rating-static-indv rating-50 margin-top-none td"></div>
                    </div>
                    <!-- REVIEW RATING - PRICING -->
                    <div class="tr margin-bottom-md">
                        <div class="lt-grey small-text td">Pricing</div>
                        <div class="rating-static-indv rating-50 margin-top-none td"></div>
                    </div>
                    <!-- REVIEW RATING - EXPERIENCE -->
                    <div class="tr margin-bottom-md">
                        <div class="td lt-grey small-text">Overall Experience</div>
                        <div class="rating-static-indv rating-50 margin-top-none td"></div>
                    </div>
                    <!-- REVIEW RATING - RECOMMEND DEALER -->
                    <div class="tr">
                        <div class="lt-grey small-text td">Recommend Dealer</div>
                        <div class="td small-text boldest">
                            Yes
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """)
        self.when_executes_buick_builder()
        self.assert_transformed_to(
            [{
                'page': 1,
                'reviews': [{
                    'date': '',
                    'employees': [],
                    'fakeLevelLabel': '',
                    'fakeLevelValue': 0,
                    'ratings': {
                        'dealRating': 50.0,
                        'customerService': 50.0,
                        'friendliness': 50.0,
                        'pricing': 50.0,
                        'overrallExperience': 50.0,
                        'recommendDealer': True
                    },
                    'text': '',
                    'title': '',
                    'user': ''
                }],
            }]
        )