*****************
Python Marketman
*****************

Python Marketman is a basic marketman.com REST API client built for Python 3.5, 3.6, 3.7 and 3.8. The goal is to provide a very low-level interface to the REST Resource, returning a dictionary of the API JSON response.

You can find out more regarding the format of the results in the `Official Marketman.com REST API Documentation`_

.. _Official Marketman.com REST API Documentation: https://api-doc.marketman.com/?version=latest



Examples
--------
To access your Marketman account, provide your API Key and API Password to your Marketman instance.

For example:

.. code-block:: python

    from python_marketman import Marketman
    mm = Marketman(api_key='', api_password='')



Inventory
---------
Access your inventory by calling the relevant method on your Marketman instance:

.. code-block:: python

    mm.get_items()



Items
-----
Access your inventory by calling the relevant method on your Marketman instance:

.. code-block:: python

    mm.get_vendors()



Authors & License
-----------------

This package is released under an open source Apache 2.0 license: Copyright 2020 Lukas Klement. It was inspired by the excellent library `Official Marketman.com REST API Documentation`_

.. _simple_salesforce: https://github.com/simple-salesforce/simple-salesforce
