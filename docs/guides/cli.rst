Command Line Interface
======================

``jugaad-data`` ships a CLI called ``jdata``, powered by
`Click <https://click.palletsprojects.com/>`_.

.. code-block:: bash

   $ jdata --help


Bhavcopies
----------

.. code-block:: bash

   # Today's equity bhavcopy
   $ jdata bhavcopy -d ./data

   # Specific date
   $ jdata bhavcopy -d ./data -f 2020-01-01

   # Date range
   $ jdata bhavcopy -d ./data -f 2020-01-01 -t 2020-01-31

   # F&O bhavcopy
   $ jdata bhavcopy -d ./data -f 2020-01-01 --fo

   # Full bhavcopy (with delivery data)
   $ jdata bhavcopy -d ./data -f 2020-01-01 --full

   # Index bhavcopy
   $ jdata bhavcopy -d ./data -f 2020-01-01 --idx


Historical Stock Data
---------------------

.. code-block:: bash

   $ jdata stock -s SBIN -f 2020-01-01 -t 2020-01-31 -o sbin.csv

   # With different series
   $ jdata stock -s HDFC -f 2020-01-01 -t 2020-01-31 -S BE -o hdfc.csv

Options:

======== ============================
Flag     Description
======== ============================
``-s``   Stock symbol (required)
``-f``   From date ``yyyy-mm-dd``
``-t``   To date ``yyyy-mm-dd``
``-S``   Series (default ``EQ``)
``-o``   Output file path
======== ============================


Historical Index Data
---------------------

.. code-block:: bash

   $ jdata index -s "NIFTY 50" -f 2020-01-01 -t 2020-01-31 -o nifty.csv


Historical Derivatives Data
----------------------------

.. code-block:: bash

   # Stock futures
   $ jdata derivatives -s SBIN -f 2020-01-01 -t 2020-01-30 \
       -e 2020-01-30 -i FUTSTK -o sbin_fut.csv

   # Stock call options
   $ jdata derivatives -s SBIN -f 2020-01-01 -t 2020-01-30 \
       -e 2020-01-30 -i OPTSTK -p 330 --ce -o sbin_ce.csv

   # Index put options
   $ jdata derivatives -s NIFTY -f 2020-01-01 -t 2020-01-23 \
       -e 2020-01-23 -i OPTIDX -p 11000 --pe -o nifty_pe.csv

Options:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Flag
     - Description
   * - ``-s``
     - Symbol (required)
   * - ``-f``
     - From date (required)
   * - ``-t``
     - To date (required)
   * - ``-e``
     - Expiry date (required)
   * - ``-i``
     - Instrument: FUTSTK/FUTIDX/OPTSTK/OPTIDX
   * - ``-p``
     - Strike price (options only)
   * - ``--ce`` / ``--pe``
     - Call / Put (options only)
   * - ``-o``
     - Output file path
