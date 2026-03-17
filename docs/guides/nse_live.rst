NSE Live Data
=============

Real-time market data from NSE using the :class:`~jugaad_data.nse.live.NSELive` class.

.. contents:: On this page
   :local:
   :depth: 2


Initialisation
--------------

.. code-block:: python

   from jugaad_data.nse import NSELive

   n = NSELive()

All methods use a time-based in-memory cache (default 5 seconds) to
avoid hitting the NSE API too frequently.


Market Status
-------------

.. code-block:: python

   status = n.market_status()
   # Returns dict with 'marketState' list — one entry per segment

   turnover = n.market_turnover()
   # Turnover across Equities, Index Futures/Options, etc.


Live Index Data
---------------

.. code-block:: python

   # All indices at a glance
   all_idx = n.all_indices()
   for idx in all_idx['data']:
       print(f"{idx['index']} — {idx['last']}")

   # Detailed view for one index
   nifty = n.live_index("NIFTY 50")

Common index names: ``NIFTY 50``, ``NIFTY BANK``, ``NIFTY IT``,
``NIFTY PHARMA``, ``INDIA VIX``, etc.


Live Stock Quotes
-----------------

.. code-block:: python

   quote = n.stock_quote("SBIN")

   # Price info
   print(quote['priceInfo']['lastPrice'])
   print(quote['priceInfo']['vwap'])

   # Company info
   print(quote['info']['companyName'])

   # Trade / order book
   trade = n.trade_info("SBIN")
   print(trade['marketDeptOrderBook']['totalBuyQuantity'])

Tick Data (Intraday)
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   ticks = n.tick_data("SBIN")
   for ts_ms, price in ticks['grapthData'][:5]:
       print(ts_ms, price)


Live Derivatives Data
---------------------

.. code-block:: python

   fno = n.stock_quote_fno("RELIANCE")

   for contract in fno['data'][:5]:
       print(f"{contract['identifier']:40} | "
             f"Price: {contract['lastPrice']:>8} | "
             f"OI: {contract['openInterest']}")

   # Filter futures
   futures = [c for c in fno['data']
              if c['instrumentType'] == 'FUTSTK']

   # Filter call options for a specific expiry
   calls = [c for c in fno['data']
            if c['optionType'] == 'CE'
            and c['expiryDate'] == '30-Mar-2026']

.. note::

   ``stock_quote_fno`` uses the NSE NextApi endpoint and returns *all*
   available contracts (futures + all expiries of calls and puts) in a
   single response.


Option Chains
-------------

.. code-block:: python

   # Index option chain (nearest expiry auto-selected)
   oc = n.index_option_chain("NIFTY")

   # With a specific expiry
   oc = n.index_option_chain("NIFTY", expiry="30-Mar-2026")

   # Equity option chain
   oc = n.equities_option_chain("RELIANCE")

   # Currency option chain
   oc = n.currency_option_chain("USDINR")

Parsing the chain:

.. code-block:: python

   for row in oc['filtered']['data']:
       ce = row['CE']['lastPrice']
       pe = row['PE']['lastPrice']
       print(f"Strike {row['strikePrice']:>8} | "
             f"CE {ce:>8} | PE {pe:>8}")


Corporate Announcements
-----------------------

.. code-block:: python

   # All recent announcements
   anns = n.corporate_announcements()

   # Filter by symbol and date range
   from datetime import date
   anns = n.corporate_announcements(
       symbol="NESCO",
       from_date=date(2024, 1, 1),
       to_date=date(2024, 1, 2))


Best Practices
--------------

* **Rate limiting** — add ``time.sleep(1)`` between successive calls
  when iterating over many symbols.
* **Error handling** — wrap calls in ``try/except`` to handle
  temporary network issues and market holidays.
* **Data validation** — check that ``'priceInfo'`` exists in the
  response before accessing nested keys.
