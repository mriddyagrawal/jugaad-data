Caching
=======

``jugaad-data`` has two caching layers built in to minimize
network requests.


Disk Cache (historical data)
----------------------------

All historical data functions (``stock_raw``, ``_stock``,
``_derivatives``, ``_index``, etc.) use a **disk-based pickle
cache** via :func:`~jugaad_data.util.cached`.

* **Location** — defaults to the OS-specific user cache directory
  (via ``appdirs``).  Override with the ``J_CACHE_DIR``
  environment variable.
* **Key** — derived from the function arguments (symbol, dates,
  etc.).
* **Invalidation** — files persist indefinitely.  Delete the cache
  directory to force fresh downloads.

.. code-block:: bash

   # Override cache dir
   export J_CACHE_DIR=/tmp/jugaad_cache

   # Check default location (macOS example)
   ls ~/Library/Caches/nsehistory-stock/


Live Cache (real-time data)
---------------------------

:class:`~jugaad_data.nse.live.NSELive` methods use an **in-memory
time-based cache** via :func:`~jugaad_data.util.live_cache`.

* **Timeout** — controlled by ``NSELive.time_out`` (default
  **5 seconds**).  Subsequent calls within this window return the
  cached value.
* **Scope** — per-instance; creating a new ``NSELive()`` starts
  with an empty cache.

.. code-block:: python

   from jugaad_data.nse import NSELive

   n = NSELive()
   n.time_out = 10  # cache for 10 seconds

   q1 = n.stock_quote("SBIN")   # network call
   q2 = n.stock_quote("SBIN")   # cached (same object)
