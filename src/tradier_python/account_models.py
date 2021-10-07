from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class OptionType(Enum):
    CALL = "call"
    PUT = "put"


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
    pdt: Pdt


class Position(BaseModel):
    cost_basis: float
    date_acquired: datetime
    id: int
    quantity: float
    symbol: str


class Positions(BaseModel):
    position: List[Position] = []


class Trade(BaseModel):
    commission: float
    description: str
    price: float
    quantity: float
    symbol: str
    trade_type: str


class Adjustment(BaseModel):
    description: str
    quantity: float


class Option(BaseModel):
    option_type: OptionType
    description: str
    quantity: float


class Journal(BaseModel):
    description: str
    quantity: float


class Event(BaseModel):
    amount: float
    date: datetime
    type: str
    trade: Optional[Trade] = None
    adjustment: Optional[Adjustment] = None
    option: Optional[Option] = None
    journal: Optional[Journal] = None


class History(BaseModel):
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
    avg_fill_price: float
    exec_quantity: float
    last_fill_price: float
    last_fill_quantity: float
    remaining_quantity: float
    create_date: datetime
    transaction_date: datetime
    class_: str = Field(..., alias="class")
    option_symbol: Optional[str] = None
    num_legs: Optional[int] = None
    strategy: Optional[str] = None
    leg: Optional[List[Leg]] = None


class Orders(BaseModel):
    order: List[Order] = []


class AccountsAPIResponse(BaseModel):
    profile: Optional[Profile] = None
    balances: Optional[Balances] = None
    positions: Optional[Positions] = None
    history: Optional[History] = None
    gainloss: Optional[Gainloss] = None
    orders: Optional[Orders] = None
    order: Optional[Order] = None
