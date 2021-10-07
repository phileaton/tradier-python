import os

import pytest

from tradier_python import TradierAPI
from tradier_python.account_models import *


@pytest.fixture
def t():
    token = os.environ["TRADIER_TOKEN"]
    account_id = os.environ["TRADIER_ACCOUNT_ID"]
    base_url = os.environ.get("TRADIER_BASE_URL")
    return TradierAPI(token=token, default_account_id=account_id, base_url=base_url)


def test_get_profile(t: TradierAPI):
    profile = t.account.profile()
    assert isinstance(profile, Profile)


def test_get_balances(t: TradierAPI):
    balances = t.account.balances()
    assert isinstance(balances, Balances)


def test_get_positions(t: TradierAPI):
    positions = t.account.positions()
    assert isinstance(positions, list)
    for p in positions:
        assert isinstance(p, Position)


def test_get_history(t: TradierAPI):
    history = t.account.history()
    assert isinstance(history, list)
    for e in history:
        assert isinstance(e, Event)


def test_get_gainloss(t: TradierAPI):
    gainloss = t.account.gainloss()
    assert isinstance(gainloss, list)
    for p in gainloss:
        assert isinstance(p, ClosedPosition)


def test_get_orders(t: TradierAPI):
    orders = t.account.orders()
    assert isinstance(orders, list)
    for o in orders:
        assert isinstance(o, Order)

    if len(orders):
        id = orders[0].id
        o = t.account.order(id)
        assert isinstance(o, Order)
