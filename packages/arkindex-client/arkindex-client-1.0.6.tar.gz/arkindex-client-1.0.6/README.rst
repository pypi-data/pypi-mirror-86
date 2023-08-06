Arkindex API Client
===================

``arkindex-client`` provides an API client to interact with Arkindex servers.

.. contents::
   :depth: 2
   :local:
   :backlinks: none

Setup
-----

Install the client using ``pip``::

   pip install arkindex-client

Usage
-----

To create a client and login using an email/password combo,
use the ``ArkindexClient.login`` helper method:

.. code:: python

   from arkindex import ArkindexClient
   cli = ArkindexClient()
   cli.login('EMAIL', 'PASSWORD')

This helper method will save the authentication token in your API client, so
that it is reused in later API requests.

If you already have an API token, you can create your client like so:

.. code:: python

   from arkindex import ArkindexClient
   cli = ArkindexClient('YOUR_TOKEN')

Making requests
^^^^^^^^^^^^^^^

To perform a simple API request, you can use the ``request()`` method. The method
takes an operation ID as a name and the operation's parameters as keyword arguments.

You can open ``https://your.arkindex/api-docs/`` to access the API documentation,
which will describe the available API endpoints, including their operation ID and
parameters.

.. code:: python

   corpus = cli.request('RetrieveCorpus', id='...')

The result will be a Python ``dict`` containing the result of the API request.
If the request returns an error, an ``apistar.exceptions.ErrorResponse`` will
be raised.

Dealing with pagination
^^^^^^^^^^^^^^^^^^^^^^^

The Arkindex client adds another helper method for paginated endpoints that
deals with pagination for you: ``ArkindexClient.paginate``. This method
returns a ``ResponsePaginator`` instance, which is a classic Python
iterator that does not perform any actual requests until absolutely needed:
that is, until the next page must be loaded.

.. code:: python

   for element in cli.paginate('ListElements', corpus=corpus['id']):
       print(element['name'])

**Warning:** Using ``list`` on a ``ResponsePaginator`` may load dozens
of pages at once and cause a big load on the server. You can use ``len`` to
get the total item count before spamming a server.

A call to ``paginate`` may produce hundreds of sub-requests depending on the size
of the dataset you're requesting. To accommodate with large datasets, and support
network or performance issues, ``paginate`` supports a ``retries`` parameter to
specify the number of sub-request it's able to run for each page in the dataset.
By default, the method will retry 5 times per page.

You may want to allow ``paginate`` to fail on some pages, for really big datasets
(errors happen). In this case, you should use the optional boolean parameter
``allow_missing_data`` (set to ``False`` by default).

Here is an example of pagination on a large dataset, allowing data loss, lowering
 retries and listing the missed pages:

.. code:: python

   elements = cli.paginate(
       'ListProcessElements',
       id='XXX',
       retries=3,
       allow_missing_data=True,
   )
   for element in elements:
       print(element['id'])

   print("Missing pages: {elements.missing}")



Using another server
^^^^^^^^^^^^^^^^^^^^

By default, the API client is set to point to the main Arkindex server at
https://arkindex.teklia.com. If you need or want to use this API client on
another server, you can use the ``base_url`` keyword argument when setting up
your API client:

.. code:: python

   cli = ArkindexClient(base_url='https://somewhere')

Handling errors
^^^^^^^^^^^^^^^

APIStar_, the underlying API client we use, does most of the error handling.
It will raise two types of exceptions:

``apistar.exceptions.ErrorResponse``
  The request resulted in a HTTP 4xx or 5xx response from the server.
``apistar.exceptions.ClientError``
  Any error that prevents the client from making the request or fetching
  the response: invalid endpoint names or URLs, unsupported content types,
  or unknown request parameters. See the exception messages for more info.

Since this API client retrieves the endpoints description from the server
using the base URL, errors can occur during the retrieval and parsing of the
API schema. If this happens, an ``arkindex.exceptions.SchemaError`` exception
will be raised.

You can handle HTTP errors and fetch more information about them using the
exception's attributes:

.. code:: python

   from apistar.exceptions import ErrorResponse
   try:
       # cli.request ...
   except ErrorResponse as e:
       print(e.title)   # "400 Bad Request"
       print(e.status_code)  # 400
       print(e.result)  # Any kind of response body the server might give

Note that by default, using ``repr()`` or ``str()`` on APIStar exceptions will
not give any useful messages; a fix in APIStar is waiting to be merged. In
the meantime, you can use Teklia's `APIStar fork`_::

   pip install git+https://gitlab.com/teklia/apistar.git

This will provide support for ``repr()`` and ``str()``, which will also
enhance error messages on unhandled exceptions.

Examples
--------

Print all folders
^^^^^^^^^^^^^^^^^

.. code:: python

   for folder in cli.paginate('ListElements', folder=True):
       print(folder['name'])

Download full logs for each Ponos task in a workflow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

   workflow = cli.request('RetrieveWorkflow', id='...')
   for task in workflow['tasks']:
       with open(task['id'] + '.txt', 'w') as f:
           f.write(cli.request('RetrieveTaskLog', id=task['id']))

.. _APIStar: http://docs.apistar.com/
.. _APIStar fork: https://gitlab.com/teklia/apistar

Linting
-------

We use `pre-commit <https://pre-commit.com/>`_ with `black <https://github.com/psf/black>`_ to automatically format the Python source code of this project.

To be efficient, you should run pre-commit before committing (hence the name...).

To do that, run once :

.. code:: shell

   pip install pre-commit
   pre-commit install

The linting workflow will now run on modified files before committing, and will fix issues for you.

If you want to run the full workflow on all the files: `pre-commit run -a`.

