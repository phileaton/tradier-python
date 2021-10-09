import os

from tradier_python import TradierAPI

if __name__ == "__main__":
    token = os.environ["TRADIER_TOKEN"]
    account_id = os.environ["TRADIER_ACCOUNT_ID"]
    t = TradierAPI(token=token, default_account_id=account_id)

    profile = t.get_profile()
    print(profile)

    balances = t.get_balances()
    print(balances)

    orders = t.get_orders()
    for o in orders:
        print(o)

    positions = t.get_positions()
    for p in positions:
        print(p)

    symbol = "SPY"
    side = "buy"
    quantity = 1
    order_type = "limit"
    limit_price = 1.00
    duration = "day"

    order = t.order_equity(
        symbol=symbol,
        side=side,
        quantity=quantity,
        order_type=order_type,
        limit_price=limit_price,
        duration=duration,
    )

    cancel_response = t.cancel_order(order.id)
    print(cancel_response)
