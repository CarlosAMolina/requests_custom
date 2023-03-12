Development
============

Steps
**********

#. Download the project and change the working directory to it:

    .. code-block:: bash

       git clone git@github.com:CarlosAMolina/requests_custom
       cd requests_custom

#. Activate pipenv and install the requirements:

    .. code-block:: bash

       python3.7 -m venv env
       source env/bin/activate
       pip install pipenv
       pipenv install pytest --dev

#. Run tox:

    .. code-block:: bash

       tox

Update docs
***********

#. Modify the files with the documentation to be updated.

#. Update docs configuration files:

   - docs/source/conf.py: update the `release` value.

#. Generate documentation:

    .. code-block:: bash

       source env/bin/activate
       cd docs
       make clean && make html

#. Push changes.
