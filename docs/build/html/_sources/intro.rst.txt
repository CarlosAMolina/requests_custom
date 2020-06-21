Introduction
============

``requests_custom`` is a package that provides common desired capabilities of the requests module configured in an easy way.

Current capabilities available:

- Custom timeout for all requests.
- Raise exception with certain HTTP status code responses.
- Retry on failure.

The current implementation has been developed in Python 3 (>= 3.6.).

Motivation
**********

The package gives a class that configures the requests module, avoiding lines of codes.

Limitations
***********

This package does not configure all the options of the module requests, only the specified previously.

References
**********

- Request module

https://requests.readthedocs.io/en/master/

- Requests configuration

https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks
