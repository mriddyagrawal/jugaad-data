BSELive — BSE Market Data
=========================

.. currentmodule:: jugaad_data.bse.live

.. autoclass:: BSELive
   :no-members:
   :no-inherited-members:

   .. rubric:: Attributes

   .. autosummary::

      ~BSELive.time_out
      ~BSELive.base_url

   .. rubric:: Core Methods

   .. autosummary::
      :toctree: bse/

      ~BSELive.get
      ~BSELive.corporate_announcements

   .. rubric:: Scrip & Symbol Lookup

   .. autosummary::
      :toctree: bse/

      ~BSELive.get_scrip_list
      ~BSELive.symbol_to_scrip_code
      ~BSELive.scrip_code_to_symbol
      ~BSELive.get_scrip_info

   .. rubric:: Announcements

   .. autosummary::
      :toctree: bse/

      ~BSELive.get_attachment_url
      ~BSELive.get_announcement_with_urls
      ~BSELive.corporate_announcements_by_symbol
