import os

import pytest

from tradier_python import TradierAPI


@pytest.fixture
def T():
    token = os.environ["TRADIER_TOKEN"]
    account_id = os.environ["ACCOUNT_ID"]
    base_url = os.environ.get("TRADIER_BASE_URL")
    return TradierAPI(token=token, default_account_id=account_id, base_url=base_url)
