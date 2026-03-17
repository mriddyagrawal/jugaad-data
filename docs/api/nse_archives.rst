NSEArchives — Bhavcopies & Daily Reports
=========================================

.. currentmodule:: jugaad_data.nse.archives

.. autoclass:: NSEDailyReports
   :no-members:
   :no-inherited-members:

   .. rubric:: Methods

   .. autosummary::
      :toctree: nse_archives/

      ~NSEDailyReports.get_daily_reports
      ~NSEDailyReports.find_file
      ~NSEDailyReports.download_file
      ~NSEDailyReports.list_available_files

---

.. autoclass:: NSEArchives
   :no-members:
   :no-inherited-members:

   .. rubric:: Bhavcopies

   .. autosummary::
      :toctree: nse_archives/

      ~NSEArchives.bhavcopy_raw
      ~NSEArchives.bhavcopy_save
      ~NSEArchives.full_bhavcopy_raw
      ~NSEArchives.full_bhavcopy_save
      ~NSEArchives.bhavcopy_fo_raw
      ~NSEArchives.bhavcopy_fo_save

   .. rubric:: Bulk Deals

   .. autosummary::
      :toctree: nse_archives/

      ~NSEArchives.bulk_deals_raw
      ~NSEArchives.bulk_deals_save

   .. rubric:: Reports

   .. autosummary::
      :toctree: nse_archives/

      ~NSEArchives.download_report
      ~NSEArchives.list_available_reports

---

.. autoclass:: NSEIndicesArchives
   :no-members:
   :no-inherited-members:

   .. rubric:: Methods

   .. autosummary::
      :toctree: nse_archives/

      ~NSEIndicesArchives.bhavcopy_index_raw
      ~NSEIndicesArchives.bhavcopy_index_save

---

Module-level Functions
----------------------

.. autosummary::
   :toctree: nse_archives/

   expiry_dates
