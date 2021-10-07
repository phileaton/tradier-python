from datetime import date
from typing import TYPE_CHECKING

from .account_models import *

if TYPE_CHECKING:
    from . import TradierAPI


class AccountEndpoint:
    """Fetch positions, balances and other account related details."""

    def __init__(self, api):
        self._api: TradierAPI = api

    def profile(self) -> Profile:
        """
        The user’s profile contains information pertaining to the user and his/her accounts. In addition to listing
        all the accounts a user has, this call should be used to create a personalized experience for your customers
        (i.e. displaying their name when they log in).
        https://documentation.tradier.com/brokerage-api/user/get-profile
        """
        url = "/v1/user/profile"
        params = {}
        data = self._api.get(url, params)
        res = APIResponse(**data)
        return res.profile

    def balances(self, account_id=None) -> Balances:
        """
        Get balances information for a specific user account. Account balances are calculated on each request during
        market hours. Each night, balance figures are reconciled with our clearing firm and used as starting point for
        the following market session.
        https://documentation.tradier.com/brokerage-api/accounts/get-account-balance
        """
        if account_id is None:
            account_id = self._api.default_account_id
        url = f"/v1/accounts/{account_id}/balances"
        params = {}
        data = self._api.get(url, params)
        res = APIResponse(**data)
        return res.balances

    def positions(self, account_id=None) -> List[Position]:
        """Get the current positions being held in an account. These positions are updated intraday via trading.
        https://documentation.tradier.com/brokerage-api/accounts/get-account-positions
        """
        if account_id is None:
            account_id = self._api.default_account_id
        url = f"/v1/accounts/{account_id}/positions"
        params = {}
        data = self._api.get(url, params)
        res = APIResponse(**data)
        return res.positions.position

    # Fails with dev account
    def history(
        self,
        account_id=None,
        page: int = None,
        limit: int = None,
        type: str = None,
        start: date = None,
        end: date = None,
        symbol: str = None,
    ) -> History:

        if account_id is None:
            account_id = self._api.default_account_id
        url = f"/v1/accounts/{account_id}/history"
        params = {
            "page": page,
            "limit": limit,
            "type": type,
            "start": start,
            "end": end,
            "symbol": symbol,
        }
        data = self._api.get(url, params)
        res = APIResponse(**data)
        return res.history

    def gainloss(
        self,
        page: int = None,
        limit: int = None,
        sort_by: str = None,
        sort: str = None,
        start: date = None,
        end: date = None,
        symbol: str = None,
        account_id=None,
    ) -> Gainloss:
        if account_id is None:
            account_id = self._api.default_account_id
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
        data = self._api.get(url, params)
        res = APIResponse(**data)
        return res.gainloss

    def orders(
        self,
        include_tags: bool = False,
        account_id=None,
    ) -> List[Order]:
        if account_id is None:
            account_id = self._api.default_account_id
        url = f"/v1/accounts/{account_id}/orders"
        params = {"includeTags": include_tags}
        data = self._api.get(url, params)
        if data.get("orders") == "null":
            data["orders"] = {"order": []}
        res = APIResponse(**data)
        return res.orders.order

    def order(
        self,
        id: str,
        include_tags: bool = False,
        account_id=None,
    ):
        if account_id is None:
            account_id = self._api.default_account_id
        url = f"/v1/accounts/{account_id}/orders"
        params = {"includeTage": include_tags}
        data = self._api.get(url, params)
        res = APIResponse(**data)
        return res.orders
