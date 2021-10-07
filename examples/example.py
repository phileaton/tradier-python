import os

from tradier_python import TradierAPI

if __name__ == "__main__":
    token = os.environ["TRADIER_TOKEN"]
    account_id = os.environ["TRADIER_ACCOUNT_ID"]
    base_url = os.environ.get("TRADIER_BASE_URL")
    t = TradierAPI(token=token, default_account_id=account_id, base_url=base_url)

    profile = t.account.profile()
    print(profile.json())

    balances = t.account.balances()
    print(balances.json())
