from typing import TYPE_CHECKING

from .market_models import *
from .util import ensure_list

if TYPE_CHECKING:
    from .tradier_api import TradierAPI


class MarketEndpoint:
    """
    Fetch quotes, chains and historical data via REST and streaming APIs.
    """

    def __init__(self, api: "TradierAPI"):
        self._api = api

    def quotes(self, symbols: str, greeks: bool = False) -> Quotes:
        """
        Get a list of symbols using a keyword lookup on the symbols description. Results are in descending order by
        average volume of the security. This can be used for simple search functions.
        """
        url = "/v1/markets/quotes"
        params = {"symbols": symbols, "greeks": greeks}

        data = self._api.get(url, params)
        res = MarketsAPIResponse(**ensure_list(data, url))
        return res.quotes

    def option_chains(
        self, symbol: str, expiration: date, greeks: bool = False
    ) -> List[OptionContract]:
        """
        Get all quotes in an option chain. Greek and IV data is included courtesy of ORATS. Please check out their APIs
        for more in-depth options data.

        Greeks/IV data is updated once per hour. This data is calculated using the ORATS APIs and is supplied directly
        from them.
        """
        url = "/v1/markets/options/chains"
        params = {
            "symbol": symbol,
            "expiration": expiration,
            "greeks": greeks,
        }

        data = self._api.get(url, params)
        res = MarketsAPIResponse(**data)
        return res.options.option

    def option_strikes(self, symbol: str, expiration: date) -> List[float]:
        """
        Get an options strike prices for a specified expiration date.
        """
        url = "/v1/markets/options/strikes"
        params = {"symbol": symbol, "expiration": expiration}

        data = self._api.get(url, params)
        res = MarketsAPIResponse(**data)
        return res.strikes.strike

    def option_expirations(
        self, symbol: str, include_all_roots: str = None, strikes: str = None
    ) -> [date]:
        """
        Get expiration dates for a particular underlying.

        Note that some underlying securities use a different symbol for their weekly options (RUT/RUTW, SPX/SPXW). To
        make sure you see all expirations, make sure to send the includeAllRoots parameter. This will also ensure any
        unique options due to corporate actions (AAPL1) are returned.
        """
        url = "/v1/markets/options/expirations"
        params = {
            "symbol": symbol,
            "includeAllRoots": include_all_roots,
            "strikes": strikes,
        }

        data = self._api.get(url, params)
        res = MarketsAPIResponse(**data)
        return res.expirations.date

    def lookup_option_symbols(self, underlying: str) -> List[Symbol]:
        """
        Get all options symbols for the given underlying. This will include additional option roots (ex. SPXW, RUTW) if applicable.
        """
        url = "/v1/markets/options/lookup"
        params = {"underlying": underlying}

        data = self._api.get(url, params)
        res = MarketsAPIResponse(**data)
        return res.symbols

    def historical_quotes(
        self, symbol: str, interval: str = None, start: date = None, end: date = None
    ) -> List[HistoricQuote]:
        """
        Get historical pricing for a security. This data will usually cover the entire lifetime of the company if
        sending reasonable start/end times. You can fetch historical pricing for options by passing the OCC option symbol
        (ex. AAPL220617C00270000) as the symbol.

        Notes: Historical data may not be dividend adjusted as this relies on the exchanges to report/adjust it properly.
        Historical options data is not available for expired options.
        """
        url = "/v1/markets/history"
        params = {"symbol": symbol, "interval": interval, "start": start, "end": end}

        data = self._api.get(url, params)
        res = MarketsAPIResponse(**data)
        return res.history.day

    def time_and_sales(
        self,
        symbol: str,
        interval: str = None,
        start: date = None,
        end: date = None,
        session_filter: str = None,
    ) -> List[TimesalesData]:
        """
        Time and Sales (timesales) is typically used for charting purposes. It captures pricing across a time slice at
        predefined intervals.

        Tick data is also available through this endpoint. This results in a very large data set for high-volume
        symbols, so the time slice needs to be much smaller to keep downloads time reasonable.
        """
        url = "/v1/markets/timesales"
        params = {
            "symbol": symbol,
            "interval": interval,
            "start": start,
            "end": end,
            "session_filter": session_filter,
        }

        data = self._api.get(url, params)
        res = MarketsAPIResponse(**data)
        return res.series.data

    def etb_list(self) -> List[Security]:
        """
        The ETB list contains securities that are able to be sold short with a Tradier Brokerage account. The list is
        quite comprehensive and can result in a long download response time.
        """
        url = "/v1/markets/etb"
        params = {}
        data = self._api.get(url, params)
        res = MarketsAPIResponse(**data)
        return res.securities.security

    def clock(self) -> Clock:
        """
        Get the intraday market status. This call will change and return information pertaining to the current day. If
        programming logic on whether the market is open/closed – this API call should be used to determine the current
        state.
        """
        url = "/v1/markets/clock"
        params = {}
        data = self._api.get(url, params)
        res = MarketsAPIResponse(**data)
        return res.clock

    def calendar(self, month: int = None, year: int = None) -> List[Hours]:
        """
        Get the market calendar for the current or given month. This can be used to plan ahead regarding strategies.
        However, the Get Intraday Status should be used to determine the current status of the market.
        """
        url = "/v1/markets/calendar"
        params = {"month": month, "year": year}
        data = self._api.get(url, params)
        res = MarketsAPIResponse(**data)
        return res.calendar.days.day

    def search_companies(self, query: str, indexes: bool = True) -> List[Security]:
        """
        Get a list of symbols using a keyword lookup on the symbols description. Results are in descending order by
        average volume of the security. This can be used for simple search functions.
        """
        url = "/v1/markets/search"
        params = {"q": query, "indexes": indexes}
        data = self._api.get(url, params)
        res = MarketsAPIResponse(**data)
        if res.securities is not None:
            return res.securities.security
        else:
            return []

    def lookup_symbol(
        self, query: str, exchanges: str = None, types: str = None
    ) -> List[Security]:
        """
        Get a list of symbols using a keyword lookup on the symbols description. Results are in descending order by
        average volume of the security. This can be used for simple search functions.
        """
        url = "/v1/markets/lookup"
        params = {"q": query, "exchanges": exchanges, "types": types}
        data = self._api.get(url, params)
        res = MarketsAPIResponse(**ensure_list(data, "securities", "security"))
        if res.securities is not None:
            return res.securities.security
        else:
            return []
