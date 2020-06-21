Examples
========

Installation
************

:code:`pip install requests_custom`

How to use
**********

.. code-block:: python

    """This example demostrates how import the class, configure the debug option
    and request an URL.
    """

    from requests_custom import requests_custom
    requests = requests_custom.RequestsCustom(debug_full=True).get_requests()
    requests.get('https://duckduckgo.com')
