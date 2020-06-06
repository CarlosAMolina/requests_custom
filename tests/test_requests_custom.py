"""Module to test the requests_custom module."""

import unittest

from requests_custom.requests_custom import RequestsCustom


class TestRequestsCustom(unittest.TestCase):
    """Main test class.

    Attributes
    ----------
    URL : str
        URL to request with GET.
    URL_DELAY : str
        The response waits X miliseconds until be sent.
    URL_TIMEOUT : str
        URL to get a timeout response.

    .. _URLs information
       https://httpstat.us/.

    """

    URL_DELAY = "https://httpstat.us/200?sleep=7000"
    URL_TIMEOUT = "https://httpstat.us/408"
    URL = "https://duckduckgo.com"

    def test_get(self):
        """Test to request an URL."""
        requests_custom = RequestsCustom(debug_simple=True).get_requests()
        requests_custom.get(self.URL)


if __name__ == "__main__":
    unittest.main()
