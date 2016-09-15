Web Scraping Example with Celery
================================

This is an example repo for some web scraping with Python and Celery.


Running the Example
-------------------

To run the example you should create a new virtual environment to install the necessary
dependencies. The following example use virtualenv-wrapper:

.. code-block:: bash

    $ mkvirtualenv celery-example -p `which python3.5`
    (celery-example) $ pip install -r requirements.txt

With the requirements installed you can run the worker:

.. code-block:: bash

    (celery-example) $ celery -A celeryapp worker

Before kicking off the tasks you need to create the directory where there output
will be stored:

.. code-block:: bash

    $ mkdir results

