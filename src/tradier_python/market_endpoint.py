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
