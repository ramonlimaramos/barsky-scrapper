from unittest import skip

class RouteSpec:
    
    def when_acess_reviews(self):
        raise NotImplementedError()

    def when_acess_no_namespace(self):
        raise NotImplementedError()

    def assert_redirect(self, **kwargs):
        raise NotImplementedError()

    def assert_ok(self):
        raise NotImplementedError()

    def assert_response_has(self, index=None, status_code=[200, 201, 202, 304], **kwargs):
        raise NotImplementedError()

    def test_api_reviews_redirection(self):
        self.when_acess_no_namespace()
        self.assert_redirect(Location='http://localhost/api/v1')
