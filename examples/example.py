import os

from tradier_python import TradierAPI

if __name__ == "__main__":
    token = os.environ["TRADIER_TOKEN"]
    account_id = os.environ["TRADIER_ACCOUNT_ID"]
    base_url = os.environ.get("TRADIER_BASE_URL")
    t = TradierAPI(token=token, default_account_id=account_id, base_url=base_url)

    profile = t.account.profile()
    print(profile)

    balances = t.account.balances()
    print(balances)

    orders = t.account.orders()
    for o in orders:
        print(o)

    positions = t.account.positions()
    for p in positions:
        print(p)

    symbol = "SPY"
    side = "buy"
    quantity = 1
    order_type = "market"
    duration = "day"

    order = t.trading.order_equity(
        symbol=symbol,
        side=side,
        quantity=quantity,
        order_type=order_type,
        duration=duration,
    )

    cancel_response = t.trading.cancel_order(order.id)
    print(cancel_response)
