## Work with the module without install it with pip.

### Requirements

- Python 3 >= 3.6

- Python3 venv

~~~
sudo apt-get install python3-venv
~~~

### Run

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
pip install ../requirements.txt
~~~

Test the module:

~~~
python requests_custom.py
~~~
