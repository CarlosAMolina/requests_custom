Module to work with custom requests capabilities.

Current capabilities configured:

- Custom timeout for all requests.
- Raise exception with certain HTTP status code responses.
- Retry on failure.

# Requirements

- Python 3

- Python3 venv

~~~
sudo apt-get install python3-venv
~~~

# Run

Create a virtual environment:

~~~
python3 -m venv env
~~~

Activate the virtual environment:

~~~
source env/bin/activate
~~~

Install requirements:

~~~
/bin/bash install_pip -p $(pwd)
~~~

Test the module:

~~~
python requests_custom.py
~~~

# References

https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/
