"""Module to test the requests_custom module."""

import unittest

from requests import exceptions
from requests_custom.requests_custom import RequestsCustom


class TestRequestsCustom(unittest.TestCase):
    """Main test class.

    Attributes
    ----------
    URL_DELAY : str
        The response waits X miliseconds until be sent.
    URL_TIMEOUT : str
        URL to get a timeout response.

    .. _URLs information
       https://httpstat.us/.

    """

    URL_DELAY = "https://httpstat.us/200?sleep=7000" # TODO test

    def setUp(self):
        self.requests_custom = RequestsCustom(debug_simple=True).get_requests()

    def test_get_url_with_a_correct_response(self):
        URL = "https://duckduckgo.com"
        response = self.requests_custom.get(URL)
        assert response.status_code == 200

    def _test_get_url_with_a_timeout_response(self):
        self.requests_custom.RETRY_ATTEMPTS = 2 # TODO not working
        URL = "https://httpstat.us/408"
        #TODO try:
        #TODO     response = self.requests_custom.get(URL)
        #TODO     assert False
        #TODO except exceptions.RetryError:
        #TODO     assert True
        #TODO except:
        #TODO     assert False


if __name__ == "__main__":
    unittest.main()
