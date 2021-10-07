from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .tradier_api import TradierAPI


class TradingEndpoint:
    """
    Place equity and complex option trades including advanced orders.
    """

    def __init__(self, api: "TradierAPI"):
        self._api = api
