import unittest

from requests_custom.requests_custom import RequestsCustom

class TestRequestsCustom(unittest.TestCase):

    def test_get_backoff_default_values(self):
        requests_custom = RequestsCustom(debug_simple=True)
        self.assertEqual([1.0, 2, 4, 8, 16], requests_custom._get_backoff())

    def test_get_backoff_custom(self):
        requests_custom = RequestsCustom(debug_simple=True)
        requests_custom.BACKOFF_FACTOR = 0
        requests_custom.RETRY_ATTEMPTS = 0
        requests_custom._log_backoff_factor()
        self.assertEqual([], requests_custom._get_backoff())
