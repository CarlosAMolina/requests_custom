"""
Python 3 >= 3.6
Module to work with custom requests capabilities.
References: see README.md.
"""

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests_toolbelt.utils import dump
import http
import requests
import sys

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
    :att debug_full: bool, activate debug the entire HTTP lifecycle.
    :att METHOD_WHITELIST: list of strs, HTTP methods to retry on. POST not included by default.
    :att RETRY_ATTEMPTS: int, total number of retry attempts to make.
    :att STATUS_FORCELIST: HTTP response codes to retry on.
    :att TIMEOUT_DEFAULT: int, timeout to use at all requests. Seconds.
    """

    def __init__(self,
                 debug_simple = False,
                 debug_full   = False):
        """
        :param debug_simple: bool, debug the requests see 
               '_set_debug_simple'.
        :param debug_full: bool, debug all requests information.
        """
        self.BACKOFF_FACTOR = 2
        self.METHOD_WHITELIST = ["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE"]
        self.RETRY_ATTEMPTS = 5
        self.STATUS_FORCELIST = [408, # Timeout.
                                 429, 500, 502, 503, 504]
        self.TIMEOUT_DEFAULT = 5
        # Show retry configuracion. Join list of ints.
        print("RequestsCustom backoff factor"
              f": {', '.join(map(str,self._get_backoff()))}")
        # Set debug.
        # Initialize attributes.
        self.debug_simple = debug_simple
        self.debug_full   = debug_full
        # Only activate one type of debug.
        if debug_simple is True:
            self._set_debug_simple()
            self.debug_full = False
        elif debug_full is True:
            self.debug_full = True

    def _set_debug_simple(self):
        """ Debug requests and headers, no response body.
        The debug information will appear too when this module is
        called from another ones.
        :param None.
        :return None.
        """
        # A value greater than 0 enables debug logging.
        http.client.HTTPConnection.debuglevel = 1


    def _logging_hook(self, response, *args, **kwargs):
        """ Debug the entire HTTP lifecycle.
        https://toolbelt.readthedocs.io/en/latest/dumputils.html
        """
        data = dump.dump_all(response)
        print(data.decode('utf-8'))

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
        # Set debug the entire HTTP lifecycle.
        if self.debug_full is True:
            http.hooks["response"] = [self._logging_hook]
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
    URL         = 'https://duckduckgo.com'

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
        requests_custom = RequestsCustom(debug_full = True).get_requests()
        requests_custom.get(self.URL)


if __name__ == '__main__':
    Test().get_url()
