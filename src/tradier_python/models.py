from datetime import date, datetime, time
from enum import Enum
from typing import Any, List, Optional

from pydantic import BaseModel, Field, validator

BROKERAGE_ENDPOINT = "https://api.tradier.com/"
SANDBOX_ENDPOINT = "https://sandbox.tradier.com/"


class OptionType(Enum):
    CALL = "call"
    PUT = "put"


class OptionType(Enum):
    CALL = "call"
    PUT = "put"

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value

    def __eq__(self, other):
        return self.value == other


class Account(BaseModel):
    account_number: str
    classification: str
    date_created: datetime
    day_trader: bool
    option_level: int
    status: str
    type: str
    last_update_date: datetime


class Profile(BaseModel):
    account: List[Account]
    id: str
    name: str

    @validator("account", pre=True)
    @classmethod
    def to_list(cls, v):
        """The API sometimes returns a single account and sometimes a list. Always return a list here for
        consistency."""
        return v if isinstance(v, list) else [v]


class Margin(BaseModel):
    fed_call: int
    maintenance_call: int
    option_buying_power: float
    stock_buying_power: float
    stock_short_value: int
    sweep: int


class Cash(BaseModel):
    cash_available: float
    sweep: int
    unsettled_funds: float


class Pdt(BaseModel):
    fed_call: int
    maintenance_call: int
    option_buying_power: float
    stock_buying_power: float
    stock_short_value: int


class Balances(BaseModel):
    option_short_value: int
    total_equity: float
    account_number: str
    account_type: str
    close_pl: float
    current_requirement: float
    equity: int
    long_market_value: float
    market_value: float
    open_pl: float
    option_long_value: float
    option_requirement: int
    pending_orders_count: int
    short_market_value: int
    stock_long_value: float
    total_cash: float
    uncleared_funds: int
    pending_cash: int
    margin: Optional[Margin]
    cash: Optional[Cash]
    pdt: Optional[Pdt]


class Position(BaseModel):
    cost_basis: float
    date_acquired: datetime
    id: int
    quantity: float
    symbol: str


class Positions(BaseModel):
    position: List[Position] = []


class TradeEvent(BaseModel):
    commission: float
    description: str
    price: float
    quantity: float
    symbol: str
    trade_type: str


class AdjustmentEvent(BaseModel):
    description: str
    quantity: float


class OptionEvent(BaseModel):
    option_type: OptionType
    description: str
    quantity: float


class JournalEvent(BaseModel):
    description: str
    quantity: float


class Event(BaseModel):
    amount: float
    date: datetime
    type: str
    trade: Optional[TradeEvent] = None
    adjustment: Optional[AdjustmentEvent] = None
    option: Optional[OptionEvent] = None
    journal: Optional[JournalEvent] = None


class AccountHistory(BaseModel):
    event: List[Event] = []


class ClosedPosition(BaseModel):
    close_date: datetime
    cost: float
    gain_loss: float
    gain_loss_percent: float
    open_date: datetime
    proceeds: float
    quantity: float
    symbol: str
    term: int


class Gainloss(BaseModel):
    closed_position: List[ClosedPosition] = []


class Leg(BaseModel):
    id: int
    type: str
    symbol: str
    side: str
    quantity: float
    status: str
    duration: str
    price: Optional[float]
    avg_fill_price: float
    exec_quantity: float
    last_fill_price: float
    last_fill_quantity: float
    remaining_quantity: float
    create_date: datetime
    transaction_date: str
    class_: str = Field(..., alias="class")
    option_symbol: Optional[str] = None


class Order(BaseModel):
    id: int
    type: str
    symbol: str
    side: str
    quantity: float
    status: str
    duration: str
    price: Optional[float] = None
    stop_price: Optional[float] = None
    avg_fill_price: float
    exec_quantity: float
    last_fill_price: float
    last_fill_quantity: float
    remaining_quantity: float
    create_date: datetime
    transaction_date: datetime
    order_class: str = Field(..., alias="class")
    option_symbol: Optional[str] = None
    num_legs: Optional[int] = None
    strategy: Optional[str] = None
    tag: Optional[str] = None
    leg: Optional[List[Leg]] = None


class Orders(BaseModel):
    order: List[Order] = []


class AccountsAPIResponse(BaseModel):
    profile: Optional[Profile] = None
    balances: Optional[Balances] = None
    positions: Optional[Positions] = None
    history: Optional[AccountHistory] = None
    gainloss: Optional[Gainloss] = None
    orders: Optional[Orders] = None
    order: Optional[Order] = None


class Greeks(BaseModel):
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float
    phi: float
    bid_iv: float
    mid_iv: float
    ask_iv: float
    smv_vol: float
    updated_at: str


class Quote(BaseModel):
    symbol: str
    description: str
    exch: str
    type: str
    last: Optional[float]
    change: Optional[float]
    volume: int
    open: Optional[float]
    high: Optional[float]
    low: Optional[float]
    close: Any
    bid: float
    ask: float
    change_percentage: Optional[float]
    average_volume: int
    last_volume: int
    trade_date: int
    prevclose: Optional[float]
    week_52_high: float
    week_52_low: float
    bidsize: int
    bidexch: str
    bid_date: datetime
    asksize: int
    askexch: str
    ask_date: datetime
    root_symbols: Optional[str] = None
    underlying: Optional[str] = None
    strike: Optional[float] = None
    open_interest: Optional[int] = None
    contract_size: Optional[int] = None
    expiration_date: Optional[date] = None
    expiration_type: Optional[str] = None
    option_type: Optional[OptionType] = None
    root_symbol: Optional[str] = None
    greeks: Optional[Greeks] = None


class UnmatchedSymbols(BaseModel):
    symbol: str


class Quotes(BaseModel):
    quotes: List[Quote] = Field(alias="quote")
    unmatched_symbols: Optional[UnmatchedSymbols]


class Options(BaseModel):
    option: List[Quote]


class Strikes(BaseModel):
    strike: List[float]


class Expirations(BaseModel):
    date: List[date]


class Symbol(BaseModel):
    rootSymbol: str
    options: List[str]


class HistoricQuote(BaseModel):
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: int


class History(BaseModel):
    day: List[HistoricQuote]


class TimesalesData(BaseModel):
    time: datetime
    timestamp: int
    price: float
    open: float
    high: float
    low: float
    close: float
    volume: int
    vwap: float


class Series(BaseModel):
    data: List[TimesalesData]


class Security(BaseModel):
    symbol: str
    exchange: str
    type: str
    description: Optional[str]


class Securities(BaseModel):
    security: List[Security]


class Clock(BaseModel):
    date: date
    description: str
    state: str
    timestamp: int
    next_change: time
    next_state: str


class Premarket(BaseModel):
    start: time
    end: time


class Open(BaseModel):
    start: time
    end: time


class Postmarket(BaseModel):
    start: time
    end: time


class Hours(BaseModel):
    date: date
    status: str
    description: str
    premarket: Optional[Premarket]
    open: Optional[Open]
    postmarket: Optional[Postmarket]


class Days(BaseModel):
    day: List[Hours]


class Calendar(BaseModel):
    month: int
    year: int
    days: Days


class MarketsAPIResponse(BaseModel):
    quotes: Optional[Quotes] = None
    options: Optional[Options] = None
    strikes: Optional[Strikes] = None
    expirations: Optional[Expirations] = None
    symbols: Optional[List[Symbol]] = None
    history: Optional[History] = None
    series: Optional[Series] = None
    securities: Optional[Securities] = None
    clock: Optional[Clock] = None
    calendar: Optional[Calendar] = None


class OrderDetails(BaseModel):
    id: str
    status: str
    partner_id: Optional[str]


class APIErrors(BaseModel):
    error_list: List[str] = Field(alias="error")


class OrderAPIResponse(BaseModel):
    order: Optional[OrderDetails]
    errors: Optional[APIErrors]
