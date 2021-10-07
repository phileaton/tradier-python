from datetime import date
from typing import TYPE_CHECKING

from .market_models import *

if TYPE_CHECKING:
    from .tradier_api import TradierAPI


class MarketEndpoint:
    """
    Place equity and complex option trades including advanced orders.
    """

    def __init__(self, api: "TradierAPI"):
        self._api = api

    def option_expirations(self, symbol: str, include_all_roots: str=None, strikes:str=None)->[date]:
        url = "/v1/markets/options/expirations"
        params = {'symbol': symbol, 'includeAllRoots': include_all_roots, 'strikes': strikes}
        data = self._api.get(url, params)
        res = MarketsAPIResponse(**data)
        return res.expirations.date