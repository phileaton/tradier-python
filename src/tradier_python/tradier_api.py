from urllib.parse import urljoin

import requests

from .account_endpoint import AccountEndpoint
from .market_endpoint import MarketEndpoint
from .trading_endpoint import TradingEndpoint


class TradierAPIError(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message


class TradierAPI:
    """
    https://documentation.tradier.com/brokerage-api
    """

    def __init__(self, token, default_account_id=None, base_url=None):

        self.default_account_id = default_account_id
        self.base_url = base_url if base_url else "https://sandbox.tradier.com/"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            }
        )
        self.account = AccountEndpoint(self)
        self.trading = TradingEndpoint(self)
        self.market = MarketEndpoint(self)

    def get(self, path: str, params: dict) -> dict:
        """makes a GET request to a particular endpoint"""
        url = urljoin(self.base_url, path)
        response = self.session.get(url, params=params)
        if response.status_code != 200:
            raise TradierAPIError(
                response.status_code, response.content.decode("utf-8")
            )
        return response.json()
