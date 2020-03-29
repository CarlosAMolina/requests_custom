"""
Python 3.6+
Module to work with custom requests capabilities.
References: see README.md.
"""

import requests
import sys
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class TimeoutHTTPAdapter(HTTPAdapter):
    """ Setting default timeouts.
    :att TIMEOUT_DEFAULT: int, timeout to use at all requests. Seconds.
    """

    TIMEOUT_DEFAULT = 5

    def __init__(self, *args, **kwargs):
        self.timeout = self.TIMEOUT_DEFAULT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)

class RequestsCustom:
    """ Apply desired modifications to the module requests.
    Current capabilities configured:
    - Custom timeout for all requests.
    - Raise exception with certain HTTP status code responses.
    - Retry on failure.
    :att BACKOFF_FACTOR: seconds to sleep between failed request,
         after the second try, see _get_backoff function.
    :att METHOD_WHITELIST: list of strs, HTTP methods to retry on. POST not included by default.
    :att RETRY_ATTEMPTS: int, total number of retry attempts to make.
    :att STATUS_FORCELIST: HTTP response codes to retry on.
    :att TIMEOUT_DEFAULT: int, timeout to use at all requests. Seconds.
    """

    def __init__(self):
        self.BACKOFF_FACTOR = 2
        self.METHOD_WHITELIST = ["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE"]
        self.RETRY_ATTEMPTS = 5
        self.STATUS_FORCELIST = [408, # Timeout.
                                 429, 500, 502, 503, 504]
        self.TIMEOUT_DEFAULT = 5
        # Show retry configuracion. Join list of ints.
        print(f"Backoff factor: {', '.join(map(str,self._get_backoff()))}")

    def _get_backoff(self):
        """ Calculate the seconds to wait betweet attempt according 
        with the class configuration.
        https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry
        For example 2 seconds means 1s, 2s, 4s... to wait between attempts.
        :param: None, class attributes are used.
        :return: list of ints, seconds to wait between each attempt.
        """
        return [self.BACKOFF_FACTOR * (2 ** (attempt - 1))
                for attempt in range(self.RETRY_ATTEMPTS)]

    def get_requests(self):
        """ Get custom request object.
        :param: None.
        :return: request object.
        """
        # Create a custom requests object, modifying the global module throws
        # an error.
        http = requests.Session()
        # Raise exception if HTTP status code is 4xx or 5xx.
        assert_status_hook = lambda response, *args, **kwargs: response.raise_for_status()
        http.hooks["response"] = [assert_status_hook]
        # Retry on failure.
        retries = Retry(total            = self.RETRY_ATTEMPTS,
                        status_forcelist = self.STATUS_FORCELIST,
                        method_whitelist = self.METHOD_WHITELIST,
                        backoff_factor   = self.BACKOFF_FACTOR,)
        # Mount it for both http and https usage
        adapter = TimeoutHTTPAdapter(timeout     = self.TIMEOUT_DEFAULT,
                                     max_retries = retries)
        http.mount("https://", adapter)
        http.mount("http://", adapter)
        return http

class Test:
    """ Class to check this module
    Tests URLS explained at https://httpstat.us/.
    :att URL_DELAY: str, the response waits X miliseconds until be sent.
    :att URL_TIMEOUT: str, URL to get a timeout response.
    """

    URL_DELAY   = 'https://httpstat.us/200?sleep=7000'
    URL_TIMEOUT = 'https://httpstat.us/408'

    def __init__(self):
        # Show modules logs.
        import logging
        # Format: https://docs.python.org/3/library/logging.html
        logging.basicConfig(format=('%(asctime)s'
                                    #'- %(filename)s %(lineno)d'
                                    ' - %(funcName)s - %(levelname)s'
                                    ' - %(message)s'),
                            level=logging.DEBUG)

    def get_url(self):
        """ Test to request an URL. """
        requests_custom = RequestsCustom().get_requests()
        requests_custom.get(self.URL_DELAY)


if __name__ == '__main__':
    Test().get_url()
