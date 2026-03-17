Quick Start
===========

This page walks through the most common tasks.  For full details, see
the :doc:`/guides/nse_historical`, :doc:`/guides/nse_live`,
:doc:`/guides/bse_data`, and :doc:`/guides/rbi_data` guides.

Download Historical Stock Data
------------------------------

.. code-block:: python

   from datetime import date
   from jugaad_data.nse import stock_df, stock_csv

   # As a pandas DataFrame
   df = stock_df(symbol="SBIN", from_date=date(2020, 1, 1),
                 to_date=date(2020, 1, 30), series="EQ")
   print(df.head())

   # Save directly to CSV
   stock_csv(symbol="SBIN", from_date=date(2020, 1, 1),
             to_date=date(2020, 1, 30), series="EQ",
             output="SBIN_Jan.csv")

Download Bhavcopies
-------------------

.. code-block:: python

   from datetime import date
   from jugaad_data.nse import bhavcopy_save, bhavcopy_fo_save

   # Equity bhavcopy
   bhavcopy_save(date(2020, 1, 1), "./")

   # Futures & Options bhavcopy
   bhavcopy_fo_save(date(2020, 1, 1), "./")

Fetch Live Stock Quotes
-----------------------

.. code-block:: python

   from jugaad_data.nse import NSELive

   n = NSELive()
   quote = n.stock_quote("SBIN")
   print(quote['priceInfo'])   # Price information
   print(quote['info'])        # Company information

Fetch Option Chains
-------------------

.. code-block:: python

   from jugaad_data.nse import NSELive

   n = NSELive()

   # Index option chain (auto-selects nearest expiry)
   oc = n.index_option_chain("NIFTY")

   # Equity option chain
   oc = n.equities_option_chain("RELIANCE")

   # Print expiry dates
   print(oc['records']['expiryDates'])

Fetch Live Derivatives Data
----------------------------

.. code-block:: python

   from jugaad_data.nse import NSELive

   n = NSELive()
   fno = n.stock_quote_fno("RELIANCE")

   for contract in fno['data'][:5]:
       print(f"{contract['identifier']:40} | "
             f"Price: {contract['lastPrice']}")

Download Historical Derivatives
-------------------------------

.. code-block:: python

   from datetime import date
   from jugaad_data.nse import derivatives_df

   # Stock futures
   df = derivatives_df(symbol="SBIN",
                       from_date=date(2020, 1, 1),
                       to_date=date(2020, 1, 30),
                       expiry_date=date(2020, 1, 30),
                       instrument_type="FUTSTK")

   # Index put options
   df = derivatives_df(symbol="NIFTY",
                       from_date=date(2020, 1, 1),
                       to_date=date(2020, 1, 30),
                       expiry_date=date(2020, 1, 30),
                       instrument_type="OPTIDX",
                       option_type="PE",
                       strike_price=12000)

Fetch RBI Rates
---------------

.. code-block:: python

   from jugaad_data.rbi import RBI

   r = RBI()
   rates = r.current_rates()
   print(rates['Policy Repo Rate'])
   print(rates['91 day T-bills'])

BSE Corporate Announcements
----------------------------

.. code-block:: python

   from jugaad_data.bse import BSELive

   bse = BSELive()

   # Fetch announcements for ICICI Bank
   result = bse.corporate_announcements_by_symbol("ICICIBANK")
   for ann in result['Table'][:3]:
       print(ann['NEWSSUB'][:80])

Command Line Interface
----------------------

.. code-block:: bash

   # Download stock data
   $ jdata stock -s SBIN -f 2020-01-01 -t 2020-01-31 -o sbin.csv

   # Download bhavcopy
   $ jdata bhavcopy -d ./data -f 2020-01-01

   # Download index data
   $ jdata index -s "NIFTY 50" -f 2020-01-01 -t 2020-01-31 -o nifty.csv

See :doc:`/guides/cli` for the full CLI reference.
