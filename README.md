Module to work with custom requests capabilities.

Current capabilities configured:

- Custom timeout for all requests.
- Raise exception with certain HTTP status code responses.
- Retry on failure.

## Installation

~~~
pip install requests_custom
~~~

## How to use

~~~
from requests_custom import requests_custom
requests = requests_custom.RequestsCustom(debug_full=True).get_requests()
requests.get('https://duckduckgo.com')
~~~

## References

https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/
