BSE Data
========

Corporate announcements, scrip information, and symbol conversion
from BSE using the :class:`~jugaad_data.bse.live.BSELive` class.

.. contents:: On this page
   :local:
   :depth: 2


Initialisation
--------------

.. code-block:: python

   from jugaad_data.bse import BSELive

   bse = BSELive()


Corporate Announcements
-----------------------

By Scrip Code
~~~~~~~~~~~~~

.. code-block:: python

   from datetime import datetime

   result = bse.corporate_announcements(
       scrip_code=532174,  # ICICI Bank
       from_date=datetime(2024, 10, 1),
       to_date=datetime(2024, 10, 31))

   for ann in result['Table'][:3]:
       print(ann['NEWSSUB'][:80])

By Symbol
~~~~~~~~~

.. code-block:: python

   result = bse.corporate_announcements_by_symbol("ICICIBANK")

With Attachment URLs
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   result = bse.get_announcement_with_urls(scrip_code=532174)

   for ann in result['Table'][:3]:
       print(ann.get('attachment_url'))
       print(ann.get('file_size_formatted'))


Scrip List
----------

.. code-block:: python

   # All active scrips
   scrips = bse.get_scrip_list(status="Active")
   print(f"Total active scrips: {len(scrips)}")

   # Filter by group
   group_a = bse.get_scrip_list(group="A", status="Active")


Symbol / Scrip Code Conversion
-------------------------------

.. code-block:: python

   # Symbol → scrip code
   code = bse.symbol_to_scrip_code("ICICIBANK")
   print(code)  # "532174"

   # Scrip code → symbol
   sym = bse.scrip_code_to_symbol("532174")
   print(sym)  # "ICICIBANK"

   # Detailed info
   info = bse.get_scrip_info("ICICIBANK")
   print(info['Scrip_Name'])
   print(info['ISIN_NUMBER'])
