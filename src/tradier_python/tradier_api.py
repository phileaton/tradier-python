from dataclasses import dataclass
from urllib.parse import urljoin

import requests

from tradier_python.models import *


class TradierAPI:
    """
    Tradier-python is a python client for interacting with the Tradier API.
    """

    def __init__(self, token, default_account_id=None, endpoint=None):

        self.default_account_id = default_account_id
        self.endpoint = endpoint if endpoint else SANDBOX_ENDPOINT
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            }
        )

    def request(self, method: str, path: str, params: dict) -> dict:
        url = urljoin(self.endpoint, path)

        response = self.session.request(method.upper(), url, params=params)

        if response.status_code != 200:
            raise TradierAPIError(
                response.status_code, response.content.decode("utf-8")
            )
        res_json = response.json()
        key = url.rsplit("/", 1)[-1]
        if res_json.get(key) == "null":
            res_json[key] = []
        return res_json

    def get(self, path: str, params: dict) -> dict:
        """makes a GET request to an endpoint"""
        return self.request("GET", path, params)

    def post(self, path: str, params: dict) -> dict:
        """makes a POST request to an endpoint"""
        return self.request("POST", path, params)

    def delete(self, path: str, params: dict):
        """makes a DELETE request to an endpoint"""
        return self.request("DELETE", path, params)

    def put(self, path: str, params):
        """makes a PUT request to an endpoint"""
        return self.request("PUT", path, params)

    def get_profile(self) -> Profile:
        """
        The user’s profile contains information pertaining to the user and his/her accounts. In addition to listing
        all the accounts a user has, this call should be used to create a personalized experience for your customers
        (i.e. displaying their name when they log in).
        https://documentation.tradier.com/brokerage-api/user/get-profile
        """
        url = "/v1/user/profile"
        data = self.get(url, {})
        res = AccountsAPIResponse(**data)
        return res.profile

    def get_balances(self, account_id=None) -> Balances:
        """
        Get balances information for a specific user account. Account balances are calculated on each request during
        market hours. Each night, balance figures are reconciled with our clearing firm and used as starting point for
        the following market session.
        https://documentation.tradier.com/brokerage-api/accounts/get-account-balance
        """
        if account_id is None:
            account_id = self.default_account_id
        url = f"/v1/accounts/{account_id}/balances"
        data = self.get(url, {})
        res = AccountsAPIResponse(**data)
        return res.balances

    def get_positions(self, account_id=None) -> List[Position]:
        """Get the current positions being held in an account. These positions are updated intraday via trading.
        https://documentation.tradier.com/brokerage-api/accounts/get-account-positions
        """
        if account_id is None:
            account_id = self.default_account_id
        url = f"/v1/accounts/{account_id}/positions"
        data = self.get(url, {})
        res = AccountsAPIResponse(**ensure_list(data, "positions"))
        return res.positions.position

    def get_history(
        self,
        account_id=None,
        page: int = None,
        limit: int = None,
        type: str = None,
        start: date = None,
        end: date = None,
        symbol: str = None,
    ) -> List[Event]:

        if account_id is None:
            account_id = self.default_account_id
        url = f"/v1/accounts/{account_id}/history"
        params = {
            "page": page,
            "limit": limit,
            "type": type,
            "start": start,
            "end": end,
            "symbol": symbol,
        }
        data = self.get(url, params)
        res = AccountsAPIResponse(**data)
        return res.history.event

    def get_gain_loss(
        self,
        page: int = None,
        limit: int = None,
        sort_by: str = None,
        sort: str = None,
        start: date = None,
        end: date = None,
        symbol: str = None,
        account_id=None,
    ) -> List[ClosedPosition]:
        if account_id is None:
            account_id = self.default_account_id
        url = f"/v1/accounts/{account_id}/gainloss"
        params = {
            "page": page,
            "limit": limit,
            "sortBy": sort_by,
            "sort": sort,
            "start": start,
            "end": end,
            "symbol": symbol,
        }
        data = self.get(url, params)
        res = AccountsAPIResponse(**data)
        return res.gainloss.closed_position

    def get_orders(
        self,
        include_tags: bool = True,
        account_id=None,
    ) -> List[Order]:
        if account_id is None:
            account_id = self.default_account_id
        url = f"/v1/accounts/{account_id}/orders"
        params = {"includeTags": include_tags}
        data = self.get(url, params)
        res = AccountsAPIResponse(**ensure_list(data, "orders"))
        return res.orders.order

    def get_order(
        self,
        id: str,
        include_tags: bool = False,
        account_id=None,
    ):
        if account_id is None:
            account_id = self.default_account_id
        url = f"/v1/accounts/{account_id}/orders/{id}"
        params = {"includeTags": include_tags}
        data = self.get(url, params)
        res = AccountsAPIResponse(**data)
        return res.order

    def order(
        self,
        order_class: str,
        symbol: str,
        order_type: str,
        duration: str,
        quantity: Optional[int],
        side: Optional[str],
        limit_price: float = None,
        stop_price: float = None,
        tag: str = None,
        account_id: str = None,
        option_symbol: str = None,
        option_symbol_0: str = None,
        side_0: str = None,
        quantity_0: int = None,
        option_symbol_1: str = None,
        side_1: str = None,
        quantity_1: int = None,
        option_symbol_2: str = None,
        side_2: str = None,
        quantity_2: int = None,
        option_symbol_3: str = None,
        side_3: str = None,
        quantity_3: int = None,
    ) -> OrderDetails:
        """
        Place an order to trade a security.
        """
        if account_id is None:
            account_id = self.default_account_id
        url = f"/v1/accounts/{account_id}/orders"
        params = {
            "class": order_class,
            "symbol": symbol,
            "option_symbol": option_symbol,
            "side": side,
            "quantity": quantity,
            "type": order_type,
            "duration": duration,
            "price": limit_price,
            "stop": stop_price,
            "tag": tag,
            "option_symbol[0]": option_symbol_0,
            "side[0]": side_0,
            "quantity[0]": quantity_0,
            "option_symbol[1]": option_symbol_1,
            "side[1]": side_1,
            "quantity[1]": quantity_1,
            "option_symbol[2]": option_symbol_2,
            "side[2]": side_2,
            "quantity[2]": quantity_2,
            "option_symbol[3]": option_symbol_3,
            "side[3]": side_3,
            "quantity[3]": quantity_3,
        }
        params = {k: v for k, v in params.items() if v is not None}
        data = self.post(url, params)
        res = OrderAPIResponse(**data)
        if res.errors:
            raise TradierOrderError(res.errors.error_list)
        return res.order

    def order_equity(
        self,
        symbol: str,
        side: str,
        quantity: int,
        order_type: str,
        duration: str,
        limit_price: float = None,
        stop_price: float = None,
        tag: str = None,
        account_id: str = None,
    ) -> OrderDetails:
        """
        Place an order to trade an equity security.
        """
        return self.order(
            order_class="equity",
            symbol=symbol,
            side=side,
            quantity=quantity,
            order_type=order_type,
            duration=duration,
            limit_price=limit_price,
            stop_price=stop_price,
            tag=tag,
            account_id=account_id,
        )

    def order_option(
        self,
        symbol: str,
        option_symbol: str,
        side: str,
        quantity: int,
        order_type: str,
        duration: str,
        limit_price: float = None,
        stop_price: float = None,
        tag: str = None,
        account_id: str = None,
    ) -> OrderDetails:
        """
        Place an order to trade a single option.
        """
        return self.order(
            order_class="option",
            symbol=symbol,
            option_symbol=option_symbol,
            side=side,
            quantity=quantity,
            order_type=order_type,
            duration=duration,
            limit_price=limit_price,
            stop_price=stop_price,
            tag=tag,
            account_id=account_id,
        )

    def order_multi_leg_option(
        self,
        symbol: str,
        order_type: str,
        duration: str,
        limit_price: float = None,
        tag: str = None,
        option_symbol_0: str = None,
        side_0: str = None,
        quantity_0: int = None,
        option_symbol_1: str = None,
        side_1: str = None,
        quantity_1: int = None,
        option_symbol_2: str = None,
        side_2: str = None,
        quantity_2: int = None,
        option_symbol_3: str = None,
        side_3: str = None,
        quantity_3: int = None,
        account_id: str = None,
    ) -> OrderDetails:
        """
        Place an order to trade a single option.
        """
        return self.order(
            order_class="multileg",
            symbol=symbol,
            side=None,
            quantity=None,
            order_type=order_type,
            duration=duration,
            limit_price=limit_price,
            stop_price=None,
            tag=tag,
            account_id=account_id,
            option_symbol_0=option_symbol_0,
            side_0=side_0,
            quantity_0=quantity_0,
            option_symbol_1=option_symbol_1,
            side_1=side_1,
            quantity_1=quantity_1,
            option_symbol_2=option_symbol_2,
            side_2=side_2,
            quantity_2=quantity_2,
            option_symbol_3=option_symbol_3,
            side_3=side_3,
            quantity_3=quantity_3,
        )

    def cancel_order(self, order_id, account_id=None) -> OrderDetails:
        """
        Cancel and order
        """
        if account_id is None:
            account_id = self.default_account_id
        url = f"/v1/accounts/{account_id}/orders/{order_id}"
        data = self.delete(url, {})
        res = OrderAPIResponse(**data)
        return res.order

    def modify_order(
        self,
        order_id,
        order_type: str = None,
        duration: str = None,
        limit_price: float = None,
        stop_price: float = None,
        account_id=None,
    ) -> OrderDetails:
        """
        Modify an order. You may change some or all of these parameters. You may not change the session of a pre/post
        market session order. Send only the parameters you would like to adjust.
        """
        if account_id is None:
            account_id = self.default_account_id
        url = f"/v1/accounts/{account_id}/orders/{order_id}"
        params = {
            "type": order_type,
            "duration": duration,
            "price": limit_price,
            "stop": stop_price,
        }
        params = {k: v for k, v in params.items() if v is not None}
        data = self.put(url, params)
        res = OrderAPIResponse(**data)
        return res.order

    def get_quotes(self, symbols: str, greeks: bool = False) -> List[Quote]:
        """
        Get a list of symbols using a keyword lookup on the symbols description. Results are in descending order by
        average volume of the security. This can be used for simple search functions.
        """
        url = "/v1/markets/quotes"
        params = {"symbols": symbols, "greeks": greeks}

        data = self.get(url, params)
        res = MarketsAPIResponse(**ensure_list(data, "quotes"))
        return res.quotes.quotes

    def get_option_chains(
        self, symbol: str, expiration: date, greeks: bool = False
    ) -> List[Quote]:
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

        data = self.get(url, params)
        res = MarketsAPIResponse(**data)
        return res.options.option

    def get_option_strikes(self, symbol: str, expiration: date) -> List[float]:
        """
        Get an options strike prices for a specified expiration date.
        """
        url = "/v1/markets/options/strikes"
        params = {"symbol": symbol, "expiration": expiration}

        data = self.get(url, params)
        res = MarketsAPIResponse(**data)
        return res.strikes.strike

    def get_option_expirations(
        self, symbol: str, include_all_roots: bool = None, strikes: str = None
    ) -> List[date]:
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

        data = self.get(url, params)
        res = MarketsAPIResponse(**data)
        return res.expirations.date

    def lookup_option_symbols(self, underlying: str) -> List[Symbol]:
        """
        Get all options symbols for the given underlying. This will include additional option roots (ex. SPXW, RUTW) if applicable.
        """
        url = "/v1/markets/options/lookup"
        params = {"underlying": underlying}

        data = self.get(url, params)
        res = MarketsAPIResponse(**data)
        return res.symbols

    def get_historical_quotes(
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

        data = self.get(url, params)
        res = MarketsAPIResponse(**data)
        return res.history.day

    def get_time_and_sales(
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

        data = self.get(url, params)
        res = MarketsAPIResponse(**data)
        return res.series.data

    def get_etb_list(self) -> List[Security]:
        """
        The ETB list contains securities that are able to be sold short with a Tradier Brokerage account. The list is
        quite comprehensive and can result in a long download response time.
        """
        url = "/v1/markets/etb"
        data = self.get(url, {})
        res = MarketsAPIResponse(**data)
        return res.securities.security

    def get_clock(self) -> Clock:
        """
        Get the intraday market status. This call will change and return information pertaining to the current day. If
        programming logic on whether the market is open/closed – this API call should be used to determine the current
        state.
        """
        url = "/v1/markets/clock"
        data = self.get(url, {})
        res = MarketsAPIResponse(**data)
        return res.clock

    def get_calendar(self, month: int = None, year: int = None) -> List[Hours]:
        """
        Get the market calendar for the current or given month. This can be used to plan ahead regarding strategies.
        However, the Get Intraday Status should be used to determine the current status of the market.
        """
        url = "/v1/markets/calendar"
        params = {"month": month, "year": year}
        data = self.get(url, params)
        res = MarketsAPIResponse(**data)
        return res.calendar.days.day

    def search_companies(self, query: str, indexes: bool = True) -> List[Security]:
        """
        Get a list of symbols using a keyword lookup on the symbols description. Results are in descending order by
        average volume of the security. This can be used for simple search functions.
        """
        url = "/v1/markets/search"
        params = {"q": query, "indexes": indexes}
        data = self.get(url, params)
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
        data = self.get(url, params)
        res = MarketsAPIResponse(**ensure_list(data, "securities", "security"))
        if res.securities is not None:
            return res.securities.security
        else:
            return []


@dataclass
class TradierAPIError(Exception):
    code: int
    message: str


@dataclass
class TradierOrderError(Exception):
    errors: List[str]


def ensure_list(data, key1, key2=None):
    """The API is inconsitent in how empty responses are returned. This ensures that we always get an empty list."""
    if key2 is None:
        key2 = key1[:-1]

    if isinstance(data[key1], list):
        data[key1] = {}
        data[key1][key2] = []
    elif data[key1].get(key2) is None:
        data[key1][key2] = []
    elif not isinstance(data[key1].get(key2), list):
        data[key1][key2] = [data[key1][key2]]
    return data
