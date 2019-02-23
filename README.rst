soda_client
=============

|Python 3.6| |travis-badge| |codefactor grade| |coveralls|

.. |Python 3.6| image:: https://img.shields.io/badge/python-3.6-brightgreen.svg
   :target: https://www.python.org/downloads/release/python-360
.. |codefactor grade| image:: https://www.codefactor.io/repository/github/soda-profiler/python-soda/badge
   :target: https://www.codefactor.io/repository/github/soda-profiler/python-soda
.. |travis-badge| image:: https://travis-ci.org/soda-profiler/python-soda.svg?branch=master
    :target: https://travis-ci.org/soda-profiler/python-soda
.. |coveralls| image:: https://coveralls.io/repos/github/soda-profiler/python-soda/badge.svg?branch=master
   :target: https://coveralls.io/github/soda-profiler/python-soda?branch=master


Installation
~~~~~~~~~~~~

.. code:: bash

   pip install soda_client

Standard example
~~~~~~~~~~~~~~~~

.. code:: python

   from soda_client import Soda

   soda = Soda(access_token, "fib_project")

   @soda.profile
   def bad_fib(n):
      if n <= 1:
          return n
      else:
          return bad_fib(n-1) + bad_fib(n-2)

   bad_fib(10)

Asynchronous example
~~~~~~~~~~~~~~~~~~~~

.. code:: python

   import asyncio
   from soda_client import Soda

   loop = asyncio.get_event_loop()
   soda = Soda(access_token, "fib_project")

   @soda.profile
   async def bad_fib(n):
      if n <= 1:
          return n
      else:
          return await bad_fib(n-1) + await bad_fib(n-2)

   loop.run_until_complete(bad_fib(10))
