Installation
============

Basic Installation
------------------

.. code-block:: bash

   pip install jugaad-data

With Pandas Support (recommended)
---------------------------------

.. code-block:: bash

   pip install jugaad-data pandas

This enables the ``_df`` functions that return :class:`pandas.DataFrame`
objects (e.g. :func:`~jugaad_data.nse.history.stock_df`).

Requirements
------------

* Python ≥ 3.9
* ``requests``, ``click``, ``appdirs``, ``beautifulsoup4``, ``lxml``, ``brotli``
* (Optional) ``pandas``, ``numpy``

.. toctree::
   :hidden:

   quickstart
