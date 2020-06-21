"""Module to work with custom requests capabilities.

Python 3 >= 3.6

"""

import http
import sys

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests_toolbelt.utils import dump
import requests


class TimeoutHTTPAdapter(HTTPAdapter):
    """Setting default timeouts.

    Attributes
    ----------
    TIMEOUT_DEFAULT : int
        Timeout to use at all requests. Seconds.

    Parameters
    ----------
    *args
        Variable length argument list.
    **kwargs
        Arbitrary keyword arguments.

    """

    TIMEOUT_DEFAULT = 5

    def __init__(self, *args, **kwargs):
        self.timeout = self.TIMEOUT_DEFAULT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        """Use timeout at the requests.

        Overrides send() method to use the default timeout if no other
        provided.

        Parameters
        ----------
        request

        **kwargs
            Arbitrary keyword arguments.

        """
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


class RequestsCustom:
    """Apply desired modifications to the module requests.

    Current capabilities configured:

    - Custom timeout for all requests.
    - Raise exception with certain HTTP status code responses.
    - Retry on failure.

    Attributes
    ----------
    BACKOFF_FACTOR : int
        Seconds to sleep between failed request,
        after the second try, see _get_backoff function.
    debug_full : bool
        Activate debug the entire HTTP lifecycle.
    debug_simple : bool
        Debug the requests with less information, see _set_debug_simple().
    METHOD_WHITELIST : list of strs
        HTTP methods to retry on. POST not included by default.
    RETRY_ATTEMPTS : int
        Total number of retry attempts to make.
    STATUS_FORCELIST
        HTTP response codes to retry on.
    TIMEOUT_DEFAULT : int
        Timeout to use at all requests. Seconds.

    Parameters
    ----------
    debug_simple
        See the attribute with the same name.
    debug_full
        See the attribute with the same name.

    """

    def __init__(self, debug_simple=False, debug_full=False):
        self.BACKOFF_FACTOR = 2
        self.METHOD_WHITELIST = [
            "HEAD",
            "GET",
            "PUT",
            "DELETE",
            "OPTIONS",
            "TRACE",
        ]
        self.RETRY_ATTEMPTS = 5
        # Status 408: timeout.
        self.STATUS_FORCELIST = [408, 429, 500, 502, 503, 504]
        self.TIMEOUT_DEFAULT = 5
        # Show retry configuracion. Join list of ints.
        print(
            "RequestsCustom backoff factor"
            f": {', '.join(map(str,self._get_backoff()))}"
        )
        # Set debug.
        # Initialize attributes.
        self.debug_simple = debug_simple
        self.debug_full = debug_full
        # Only activate one type of debug.
        if debug_simple is True:
            self._set_debug_simple()
            self.debug_full = False
        elif debug_full is True:
            self.debug_full = True

    def _set_debug_simple(self):
        """Debug requests and headers, no response body.

        The debug information will appear too when this module is
        called from another ones.

        """
        # A value greater than 0 enables debug logging.
        http.client.HTTPConnection.debuglevel = 1

    def _logging_hook(self, response, *args, **kwargs):
        """Debug the entire HTTP lifecycle.

        Parameters
        ----------
        response
        *args
        **kwargs

        ..https://toolbelt.readthedocs.io/en/latest/dumputils.html

        """
        data = dump.dump_all(response)
        print(data.decode("utf-8"))

    def _get_backoff(self):
        """Calculate the seconds to wait betweet attempt.

        These values are calculated according with the class configuration.
        For example 2 seconds means 1s, 2s, 4s... to wait between attempts.

        Returns
        -------
        list of ints
            Seconds to wait between each attempt.

        ..https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry

        """
        return [
            self.BACKOFF_FACTOR * (2 ** (attempt - 1))
            for attempt in range(self.RETRY_ATTEMPTS)
        ]

    def get_requests(self):
        """Get custom request object.

        Returns
        -------
        request object

        """
        # Create a custom requests object, modifying the global module throws
        # an error.
        http = requests.Session()
        # Raise exception if HTTP status code is 4xx or 5xx.
        assert_status_hook = (
            lambda response, *args, **kwargs: response.raise_for_status()
        )
        http.hooks["response"] = [assert_status_hook]
        # Set debug the entire HTTP lifecycle.
        if self.debug_full is True:
            http.hooks["response"] = [self._logging_hook]
        # Retry on failure.
        retries = Retry(
            total=self.RETRY_ATTEMPTS,
            status_forcelist=self.STATUS_FORCELIST,
            method_whitelist=self.METHOD_WHITELIST,
            backoff_factor=self.BACKOFF_FACTOR,
        )
        # Mount it for both http and https usage
        adapter = TimeoutHTTPAdapter(
            timeout=self.TIMEOUT_DEFAULT, max_retries=retries
        )
        http.mount("https://", adapter)
        http.mount("http://", adapter)
        return http


if __name__ == "__main__":
    print(__doc__)
