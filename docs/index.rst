jugaad-data
===========

A Python library for downloading historical and live stock market data
from **NSE**, **BSE**, and economic data from **RBI**.

.. note::

   This library targets the *new* NSE website API, making it more
   future-proof than libraries built on the legacy NSE website.

Key Features
------------

* Download **bhavcopies** (equity, F&O, index)
* Fetch **historical OHLC** data for stocks, indices, and derivatives
* Get **live quotes**, option chains, and market turnover
* Access **RBI** monetary policy rates and T-bill yields
* **BSE** corporate announcements and scrip information
* Optional **pandas** DataFrame output
* Powerful **CLI** — ``jdata`` command for non-coders
* Built-in **caching** to avoid unnecessary network requests

.. toctree::
   :maxdepth: 2
   :hidden:

   getting_started/index
   guides/index
   api/index
   changelog
