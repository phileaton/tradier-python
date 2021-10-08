from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel

if TYPE_CHECKING:
    from .tradier_api import TradierAPI


class OrderDetails(BaseModel):
    id: str
    status: str
    partner_id: Optional[str]


class OrderAPIResponse(BaseModel):
    order: OrderDetails


class TradingEndpoint:
    """
    Place equity and complex option trades including advanced orders.
    """

    def __init__(self, api: "TradierAPI"):
        self._api = api

    def order(
        self,
        order_class: str,
        symbol: str,
        side: str,
        quantity: int,
        order_type: str,
        duration: str,
        limit_price: float = None,
        stop_price: float = None,
        tag: str = None,
        account_id: str = None,
        option_symbol: str = None,
        option_symbol_1: str = None,
        side_1: str = None,
        quantity_1: int = None,
        option_symbol_2: str = None,
        side_2: str = None,
        quantity_2: int = None,
        option_symbol_3: str = None,
        side_3: str = None,
        quantity_3: int = None,
        option_symbol_4: str = None,
        side_4: str = None,
        quantity_4: int = None,
    ) -> OrderDetails:
        """
        Place an order to trade a security.
        """
        if account_id is None:
            account_id = self._api.default_account_id
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
            "option_symbol[1]": option_symbol_1,
            "side[1]": side_1,
            "quantity[1]": quantity_1,
            "option_symbol[2]": option_symbol_2,
            "side[2]": side_2,
            "quantity[2]": quantity_2,
            "option_symbol[3]": option_symbol_3,
            "side[3]": side_3,
            "quantity[3]": quantity_3,
            "option_symbol[4]": option_symbol_4,
            "side[4]": side_4,
            "quantity[4]": quantity_4,
        }
        params = {k: v for k, v in params.items() if v is not None}
        data = self._api.post(url, params)
        res = OrderAPIResponse(**data)
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

    def cancel_order(self, order_id, account_id=None) -> OrderDetails:
        """
        Cancel and order
        """
        if account_id is None:
            account_id = self._api.default_account_id
        url = f"/v1/accounts/{account_id}/orders/{order_id}"
        data = self._api.delete(url, {})
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
            account_id = self._api.default_account_id
        url = f"/v1/accounts/{account_id}/orders/{order_id}"
        params = {
            "type": order_type,
            "duration": duration,
            "price": limit_price,
            "stop": stop_price,
        }
        params = {k: v for k, v in params.items() if v is not None}
        data = self._api.put(url, params)
        res = OrderAPIResponse(**data)
        return res.order
