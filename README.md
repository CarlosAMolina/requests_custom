Package to work with custom requests capabilities.

Current capabilities available:

- Custom timeout for all requests.
- Raise exception with certain HTTP status code responses.
- Retry on failure.

## Installation

~~~
pip install requests_custom
~~~

Pypi link: https://pypi.org/project/requests-custom/

## How to use

~~~
from requests_custom import requests_custom
requests = requests_custom.RequestsCustom(debug_full=True).get_requests()
requests.get('https://duckduckgo.com')
~~~

## Documentation

https://requests-custom.readthedocs.io/en/latest/

At the previous link you can see the references of this project.

