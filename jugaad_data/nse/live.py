"""
NSE live market data.

Provides the :class:`NSELive` class for fetching real-time stock
quotes, index data, option chains, market status, derivative
turnover, and corporate announcements from NSE.
"""
from datetime import datetime
from requests import Session
from ..util import live_cache
class NSELive:
    """Real-time data client for NSE.

    Maintains an HTTP session with browser-like headers and uses
    :func:`~jugaad_data.util.live_cache` to avoid hitting NSE too
    frequently (configurable via :attr:`time_out`).

    Example::

        >>> from jugaad_data.nse import NSELive
        >>> n = NSELive()
        >>> quote = n.stock_quote("SBIN")
        >>> print(quote['priceInfo']['lastPrice'])
        1063.2
    """
    time_out = 5
    base_url = "https://www.nseindia.com/api"
    nextapi_url = "https://www.nseindia.com/api/NextApi/apiClient/GetQuoteApi"
    page_url = "https://www.nseindia.com/get-quotes/equity?symbol=LT"
    _routes = {
            "stock_meta": "/equity-meta-info",
            "stock_quote": "/quote-equity",
            "stock_derivative_quote": "/quote-derivative",
            "stock_derivatives_data": "/NextApi/apiClient/GetQuoteApi",
            "market_status": "/marketStatus",
            "chart_data": "/chart-databyindex",
            "market_turnover": "/market-turnover",
            "equity_derivative_turnover": "/equity-stock",
            "all_indices": "/allIndices",
            "live_index": "/equity-stockIndices",
            "option_chain_v3": "/option-chain-v3",
            "option_chain_contract_info": "/option-chain-contract-info",
            "currency_option_chain": "/option-chain-currency",
            "pre_open_market": "/market-data-pre-open",
            "holiday_list": "/holiday-master?type=trading",
            "corporate_announcements": "/corporate-announcements"
    }
    
    def __init__(self):
        self.s = Session()
        h = {
            "Host": "www.nseindia.com",
            "Referer": "https://www.nseindia.com/get-quotes/equity?symbol=SBIN",
            "X-Requested-With": "XMLHttpRequest",
            "pragma": "no-cache",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36",
            "Sec-CH-UA": '"Google Chrome";v="134", "Chromium";v="134", "Not?A_Brand";v="99"',
            "Sec-CH-UA-Mobile": "?0",
            "Sec-CH-UA-Platform": '"Windows"',
            "DNT": "1",
            "Upgrade-Insecure-Requests": "1",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            }
        self.s.headers.update(h)
        self.s.get(self.page_url)

    def get(self, route, payload={}):
        """Fetch JSON data from an NSE API route.

        Args:
            route: Key into :attr:`_routes`.
            payload: Query-string parameters.

        Returns:
            dict: Parsed JSON response.
        """
        url = self.base_url + self._routes[route]
        r = self.s.get(url, params=payload)
        return r.json()

    def _get_nextapi(self, function_name, **params):
        """Call NextApi endpoint with functionName and additional parameters.
        
        Args:
            function_name: The functionName parameter for NextApi
            **params: Additional query parameters
        
        Returns:
            Parsed JSON response from NextApi
        """
        query_params = {"functionName": function_name}
        query_params.update(params)
        r = self.s.get(self.nextapi_url, params=query_params)
        return r.json()

    @live_cache
    def stock_quote(self, symbol):
        """Get a detailed live quote for a stock.

        Args:
            symbol: NSE stock symbol, e.g. ``"SBIN"``.

        Returns:
            dict: Keys include ``priceInfo``, ``info``, ``metadata``,
            ``securityInfo``, ``preOpenMarket``.
        """
        data = {"symbol": symbol}
        return self.get("stock_quote", data) 

    @live_cache
    def stock_quote_fno(self, symbol):
        """Fetch live derivatives (futures & options) data for a symbol.

        Args:
            symbol (str): Stock/Index symbol (e.g., ``'HDFC'``, ``'NIFTY'``).

        Returns:
            dict: Derivatives data with keys:

            - ``data`` – list of contract dicts, each containing
              ``identifier``, ``instrumentType`` (OPTSTK/FUTSTK),
              ``underlying``, ``expiryDate``, ``optionType`` (CE/PE/XX),
              ``strikePrice``, ``lastPrice``, ``openInterest``,
              ``totalTradedVolume``, ``openPrice``, ``highPrice``,
              ``lowPrice``, ``changeInOpenInterest``, and more.
            - ``timestamp`` – data timestamp string.

        Note:
            Uses the NSE NextApi endpoint (``getSymbolDerivativesData``).
            Returns all available contracts for the given symbol.
        """
        return self._get_nextapi("getSymbolDerivativesData", symbol=symbol)

    @live_cache
    def trade_info(self, symbol):
        """Get trade information (order book, delivery) for a stock.

        Args:
            symbol: NSE stock symbol.

        Returns:
            dict: Keys include ``bulkBlockDeals``, ``marketDeptOrderBook``,
            ``securityWiseDP``.
        """
        data = {"symbol": symbol, "section": "trade_info"}
        return self.get("stock_quote", data) 

    @live_cache
    def market_status(self):
        """Get the current status of all NSE market segments.

        Returns:
            dict: Contains ``marketState`` list with status per segment.
        """
        return self.get("market_status", {})

    @live_cache
    def chart_data(self, symbol, indices=False):
        """Get intraday chart data (timestamp, price pairs).

        Args:
            symbol: Stock symbol or index name.
            indices: Set ``True`` for index data.

        Returns:
            dict: Contains ``grapthData`` (list of ``[timestamp_ms, price]``).
        """
        data = {"index" : symbol + "EQN"}
        if indices:
            data["index"] = symbol
            data["indices"] = "true"
        return self.get("chart_data", data)
    
    @live_cache
    def tick_data(self, symbol, indices=False):
        """Alias for :meth:`chart_data`."""
        return self.chart_data(symbol, indices)

    @live_cache
    def market_turnover(self):
        """Get turnover across all market segments."""
        return self.get("market_turnover")

    @live_cache
    def eq_derivative_turnover(self, type="allcontracts"):
        """Get equity derivative turnover data.

        Args:
            type: Filter type (default ``"allcontracts"``).
        """
        data = {"index": type}
        return self.get("equity_derivative_turnover", data)
    
    @live_cache
    def all_indices(self):
        """Get data for all NSE indices.

        Returns:
            dict: Keys include ``data`` (list of indices), ``advances``,
            ``declines``, ``unchanged``.
        """
        return self.get("all_indices")

    def live_index(self, symbol="NIFTY 50"):
        """Get detailed data for a specific index.

        Args:
            symbol: Index name, e.g. ``"NIFTY 50"``, ``"NIFTY BANK"``.

        Returns:
            dict: Keys include ``name``, ``data``, ``advance``,
            ``marketStatus``.
        """
        data = {"index" : symbol}
        return self.get("live_index", data)
    
    @live_cache
    def option_chain_contract_info(self, symbol):
        """Get available expiry dates and strike prices for an option chain symbol."""
        data = {"symbol": symbol}
        return self.get("option_chain_contract_info", data)

    @live_cache
    def index_option_chain(self, symbol="NIFTY", expiry=None):
        """Fetch option chain data for index.
        
        Args:
            symbol: Index symbol (e.g., 'NIFTY', 'BANKNIFTY')
            expiry: Optional expiry date in format 'DD-MMM-YYYY' (e.g., '30-Mar-2026')
                   If not provided, fetches contract info to get the nearest expiry
        """
        # If expiry is not provided, get the nearest one
        if not expiry:
            contract_info = self.option_chain_contract_info(symbol)
            if contract_info.get("expiryDates"):
                expiry = contract_info["expiryDates"][0]
        
        # Fetch option chain data
        data = {"type": "Indices", "symbol": symbol}
        if expiry:
            data["expiry"] = expiry
        
        return self.get("option_chain_v3", data)

    @live_cache
    def equities_option_chain(self, symbol, expiry=None):
        """Fetch option chain data for equity.
        
        Args:
            symbol: Stock symbol (e.g., 'RELIANCE', 'INFY')
            expiry: Optional expiry date in format 'DD-MMM-YYYY' (e.g., '27-Mar-2026')
                   If not provided, fetches contract info to get the nearest expiry
        """
        # If expiry is not provided, get the nearest one
        if not expiry:
            contract_info = self.option_chain_contract_info(symbol)
            if contract_info.get("expiryDates"):
                expiry = contract_info["expiryDates"][0]
        
        # Fetch option chain data
        data = {"type": "Equity", "symbol": symbol}
        if expiry:
            data["expiry"] = expiry
        
        return self.get("option_chain_v3", data)

    @live_cache
    def currency_option_chain(self, symbol="USDINR"):
        data = {"symbol": symbol}
        return self.get("currency_option_chain", data)

    @live_cache
    def live_fno(self):
        """Get live data for all securities in F&O segment."""
        return self.live_index("SECURITIES IN F&O")
    
    @live_cache
    def pre_open_market(self, key="NIFTY"):
        """Get pre-open market data.

        Args:
            key: Market segment key (default ``"NIFTY"``).
        """
        data = {"key": key}
        return self.get("pre_open_market", data)
    
    @live_cache
    def holiday_list(self):
        """Get the NSE trading holiday list."""
        return self.get("holiday_list", {})

    def corporate_announcements(self, segment='equities', from_date=None, to_date=None, symbol=None):
        """
            This function returns the corporate annoucements 
            (https://www.nseindia.com/companies-listing/corporate-filings-announcements)
        """

        #from_date: 02-12-2024
        #to_date: 06-12-2024
        #symbol: 
        payload = {"index": segment}

        if from_date and to_date:
            payload['from_date'] = from_date.strftime("%d-%m-%Y")
            payload['to_date']   = to_date.strftime("%d-%m-%Y")
        elif from_date or to_date:
            raise Exception("Please provide both from_date and to_date")
        if symbol:
            payload['symbol'] = symbol
        return self.get("corporate_announcements", payload)

