RBI Economic Data
=================

Fetch current monetary policy rates, T-bill yields, and other
key economic indicators from the Reserve Bank of India website
using the :class:`~jugaad_data.rbi.RBI` class.

.. contents:: On this page
   :local:
   :depth: 2


Current Rates
-------------

.. code-block:: python

   from jugaad_data.rbi import RBI

   r = RBI()
   rates = r.current_rates()
   print(rates)

The returned dictionary includes (where available):

**Monetary Policy Rates**

* ``Policy Repo Rate`` — rate at which RBI lends to banks
* ``Marginal Standing Facility Rate`` — emergency overnight rate

**Government Securities & T-Bills**

* ``91 day T-bills``
* ``182 day T-bills``
* ``364 day T-bills``

**Banking Rates**

* ``Savings Deposit Rate``
* ``Base Rate``


Parsing Rate Values
-------------------

Values are returned as strings.  Parse them as needed:

.. code-block:: python

   def parse_pct(rate_str):
       """'4.00%' → 4.0"""
       return float(rate_str.replace('%', ''))

   repo = parse_pct(rates['Policy Repo Rate'])

   # Range values like '7.40% - 8.80%'
   def parse_range(rate_str):
       lo, hi = rate_str.split(' - ')
       return parse_pct(lo), parse_pct(hi)


Limitations
-----------

* **Snapshot only** — returns the latest published rates, no
  historical data.
* **Availability** — Monetary policy rates change quarterly;
  T-bill yields change daily after auctions.
* **Web scraping** — if RBI changes their page layout, this module
  may need updating.
