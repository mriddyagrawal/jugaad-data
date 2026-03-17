NSE Historical Data
===================

A guide to downloading historical market data from NSE — stocks,
indices, derivatives, and bhavcopies.

.. contents:: On this page
   :local:
   :depth: 2


Bhavcopies
----------

Bhavcopies are daily market snapshots published by NSE after market
close. They contain OHLC prices for all traded contracts.

Format Changes (July 8, 2024)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On July 8 2024 NSE switched from ZIP-based bhavcopies to the
**Unified Distilled File Format (UDiff)**.  The library handles both
formats automatically — no action needed on your part.

* **≥ July 8, 2024** — UDiff format via the daily-reports API.
* **< July 8, 2024** — BHAVDATA-FULL CSV with delivery data.

Equity Bhavcopy
~~~~~~~~~~~~~~~

.. code-block:: python

   from datetime import date
   from jugaad_data.nse import bhavcopy_save

   bhavcopy_save(date(2020, 1, 1), "/path/to/directory")

Output file: ``cm01Jan2020bhav.csv``

Full Bhavcopy (with Delivery Data)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from jugaad_data.nse import full_bhavcopy_save

   full_bhavcopy_save(date(2020, 1, 1), "/path/to/directory")

F&O Bhavcopy
~~~~~~~~~~~~

.. code-block:: python

   from jugaad_data.nse import bhavcopy_fo_save

   bhavcopy_fo_save(date(2020, 1, 1), "/path/to/directory")

Output file: ``fo01Jan2020bhav.csv``

Index Bhavcopy
~~~~~~~~~~~~~~

.. code-block:: python

   from jugaad_data.nse import bhavcopy_index_save

   bhavcopy_index_save(date(2020, 1, 1), "/path/to/directory")

NSE Daily Reports (39+ types)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

NSE publishes 39+ report types daily.  Use
:meth:`~jugaad_data.nse.archives.NSEArchives.list_available_reports`
and
:meth:`~jugaad_data.nse.archives.NSEArchives.download_report`
to discover and download them.

.. code-block:: python

   from jugaad_data.nse.archives import NSEArchives

   nse = NSEArchives()

   # List available reports
   reports = nse.list_available_reports()
   for key, info in reports.items():
       print(f"{key}: {info['displayName']}")

   # Download a report
   info = nse.download_report('CM-VOLATILITY', '/path/to/save')
   print(f"Saved: {info['file_path']}")


Historical Stock Data
---------------------

As a DataFrame
~~~~~~~~~~~~~~

.. code-block:: python

   from datetime import date
   from jugaad_data.nse import stock_df

   df = stock_df(symbol="SBIN",
                 from_date=date(2020, 1, 1),
                 to_date=date(2020, 1, 30),
                 series="EQ")
   print(df.head())

**Columns returned:**

=============== ======================================
Column          Description
=============== ======================================
DATE            Trading date
SERIES          Series type (``EQ``, ``BE``, etc.)
OPEN            Opening price
HIGH            Day high
LOW             Day low
PREV. CLOSE     Previous closing price
LTP             Last traded price
CLOSE           Closing price
VWAP            Volume-weighted average price
VOLUME          Total traded volume
VALUE           Total traded value
NO OF TRADES    Number of trades
DELIVERY QTY    Delivery quantity
DELIVERY %      Delivery percentage
SYMBOL          Stock symbol
=============== ======================================

As a CSV File
~~~~~~~~~~~~~

.. code-block:: python

   from jugaad_data.nse import stock_csv

   stock_csv(symbol="SBIN",
             from_date=date(2020, 1, 1),
             to_date=date(2020, 1, 30),
             series="EQ",
             output="SBIN_Jan.csv")

Series Types
~~~~~~~~~~~~

=====  =================================
Code   Description
=====  =================================
EQ     Equity (default, main series)
BE     Bulk/Block deals
GR     Group contracts
ST     Stock lending & borrowing
=====  =================================


Historical Index Data
---------------------

.. code-block:: python

   from datetime import date
   from jugaad_data.nse import index_df, index_csv

   df = index_df(symbol="NIFTY 50",
                 from_date=date(2020, 1, 1),
                 to_date=date(2020, 1, 30))

   # Or save to CSV
   index_csv(symbol="NIFTY 50",
             from_date=date(2020, 1, 1),
             to_date=date(2020, 1, 30),
             output="NIFTY50_Jan.csv")

**Columns:** Index Name, INDEX_NAME, HistoricalDate, OPEN, HIGH, LOW,
CLOSE.


Historical Derivatives Data
----------------------------

Expiry Dates
~~~~~~~~~~~~

.. code-block:: python

   from datetime import date
   from jugaad_data.nse import expiry_dates

   # All expiry dates available on a specific date
   dts = expiry_dates(date(2020, 9, 28))

   # Filter by instrument and symbol
   dts = expiry_dates(date(2020, 9, 28), "FUTIDX", "NIFTY")

**Instrument types:**

========  =================
Code      Description
========  =================
FUTSTK    Stock futures
FUTIDX    Index futures
OPTSTK    Stock options
OPTIDX    Index options
========  =================

Stock Futures
~~~~~~~~~~~~~

.. code-block:: python

   from datetime import date
   from jugaad_data.nse import derivatives_df

   df = derivatives_df(symbol="SBIN",
                       from_date=date(2020, 1, 1),
                       to_date=date(2020, 1, 30),
                       expiry_date=date(2020, 1, 30),
                       instrument_type="FUTSTK")

Stock Options
~~~~~~~~~~~~~

.. code-block:: python

   df = derivatives_df(symbol="SBIN",
                       from_date=date(2020, 1, 1),
                       to_date=date(2020, 1, 30),
                       expiry_date=date(2020, 1, 30),
                       instrument_type="OPTSTK",
                       option_type="CE",
                       strike_price=300)

Index Futures
~~~~~~~~~~~~~

.. code-block:: python

   df = derivatives_df(symbol="NIFTY",
                       from_date=date(2020, 1, 1),
                       to_date=date(2020, 1, 30),
                       expiry_date=date(2020, 1, 30),
                       instrument_type="FUTIDX")

Index Options
~~~~~~~~~~~~~

.. code-block:: python

   df = derivatives_df(symbol="NIFTY",
                       from_date=date(2020, 1, 1),
                       to_date=date(2020, 1, 30),
                       expiry_date=date(2020, 1, 30),
                       instrument_type="OPTIDX",
                       option_type="PE",
                       strike_price=12000)

.. note::

   Historical derivatives data availability depends on NSE's data
   retention policies.  Very old data (> 6 months) may not be
   available.


Best Practices
--------------

Error Handling
~~~~~~~~~~~~~~

.. code-block:: python

   from datetime import date
   from jugaad_data.nse import stock_df

   def safe_download(symbol, from_date, to_date):
       try:
           df = stock_df(symbol, from_date, to_date)
           if df.empty:
               print(f"No data for {symbol}")
               return None
           return df
       except Exception as e:
           print(f"Error: {e}")
           return None

Date Format
~~~~~~~~~~~

All dates must be :class:`datetime.date` objects:

.. code-block:: python

   from datetime import date

   # Correct
   from_date = date(2020, 1, 1)

   # Wrong — do NOT use strings
   # from_date = "2020-01-01"
