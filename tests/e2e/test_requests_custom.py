import unittest

from requests import exceptions
from requests_custom.requests_custom import RequestsCustom


class TestRequestsCustom(unittest.TestCase):
    """

    .. _URLs information
       https://httpstat.us/.

    """

    def test_get_url_with_a_correct_response_works(self):
        requests_custom = RequestsCustom(debug_simple=True).get_requests()
        URL = "https://duckduckgo.com"
        response = requests_custom.get(URL)
        self.assertEqual(200, response.status_code)

    def test_get_url_with_a_timeout_response_raises_an_exception(self):
        requests_custom = RequestsCustom(debug_simple=True)
        requests_custom.RETRY_ATTEMPTS = 1
        requests_custom.BACKOFF_FACTOR = 0
        requests_custom._log_backoff_factor()
        requests_custom = requests_custom.get_requests()
        URL = "https://httpstat.us/408"
        try:
            requests_custom.get(URL)
            raise Exception("Expected RetryError exception not raised")
        except exceptions.RetryError:
            self.assertTrue(True)

    def test_get_url_with_a_delayed_response_fails(self):
        requests_custom = RequestsCustom(debug_simple=True)
        requests_custom.RETRY_ATTEMPTS = 0
        requests_custom.BACKOFF_FACTOR = 0
        requests_custom.TIMEOUT_DEFAULT = 0.1
        requests_custom._log_backoff_factor()
        requests_custom = requests_custom.get_requests()
        URL = "https://httpstat.us/200?sleep={miliseconds}".format(miliseconds=200)
        try:
            requests_custom.get(URL)
            raise Exception("Expected RetryError exception not raised")
        except exceptions.ConnectionError:
            self.assertTrue(True)

    def test_get_url_with_a_delayed_response_works(self):
        requests_custom = RequestsCustom(debug_simple=True)
        requests_custom.RETRY_ATTEMPTS = 0
        requests_custom.BACKOFF_FACTOR = 0
        requests_custom.TIMEOUT_DEFAULT = 1
        requests_custom._log_backoff_factor()
        requests_custom = requests_custom.get_requests()
        URL = "https://httpstat.us/200?sleep={miliseconds}".format(miliseconds=100)
        response = requests_custom.get(URL)
        self.assertEqual(200, response.status_code)


if __name__ == "__main__":
    unittest.main()
