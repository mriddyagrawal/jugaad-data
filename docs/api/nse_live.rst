NSELive — Live Market Data
==========================

.. currentmodule:: jugaad_data.nse.live

.. autoclass:: NSELive
   :no-members:
   :no-inherited-members:

   .. rubric:: Attributes

   .. autosummary::

      ~NSELive.time_out
      ~NSELive.base_url

   .. rubric:: Core Methods

   .. autosummary::
      :toctree: nse_live/

      ~NSELive.get
      ~NSELive.stock_quote
      ~NSELive.trade_info
      ~NSELive.market_status

   .. rubric:: Index Data

   .. autosummary::
      :toctree: nse_live/

      ~NSELive.all_indices
      ~NSELive.live_index

   .. rubric:: Derivatives & Option Chains

   .. autosummary::
      :toctree: nse_live/

      ~NSELive.stock_quote_fno
      ~NSELive.option_chain_contract_info
      ~NSELive.index_option_chain
      ~NSELive.equities_option_chain
      ~NSELive.currency_option_chain
      ~NSELive.live_fno

   .. rubric:: Market Data

   .. autosummary::
      :toctree: nse_live/

      ~NSELive.chart_data
      ~NSELive.tick_data
      ~NSELive.market_turnover
      ~NSELive.eq_derivative_turnover
      ~NSELive.pre_open_market

   .. rubric:: Other

   .. autosummary::
      :toctree: nse_live/

      ~NSELive.holiday_list
      ~NSELive.corporate_announcements
