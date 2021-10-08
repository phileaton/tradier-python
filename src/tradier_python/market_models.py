from datetime import date, datetime, time
from typing import Any, List, Optional

from pydantic import BaseModel, Field

from .account_models import OptionType


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
    bid_date: int
    asksize: int
    askexch: str
    ask_date: int
    root_symbols: Optional[str] = None
    underlying: Optional[str] = None
    strike: Optional[float] = None
    open_interest: Optional[int] = None
    contract_size: Optional[int] = None
    expiration_date: Optional[str] = None
    expiration_type: Optional[str] = None
    option_type: Optional[OptionType] = None
    root_symbol: Optional[str] = None


class UnmatchedSymbols(BaseModel):
    symbol: str


class Quotes(BaseModel):
    quotes: List[Quote] = Field(alias="quote")
    unmatched_symbols: Optional[UnmatchedSymbols]


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


class OptionContract(BaseModel):
    symbol: str
    description: str
    exch: str
    type: str
    last: Any
    change: Any
    volume: int
    open: Any
    high: Any
    low: Any
    close: Any
    bid: float
    ask: float
    underlying: str
    strike: float
    change_percentage: Any
    average_volume: int
    last_volume: int
    trade_date: int
    prevclose: Any
    week_52_high: float
    week_52_low: float
    bidsize: int
    bidexch: str
    bid_date: int
    asksize: int
    askexch: str
    ask_date: int
    open_interest: int
    contract_size: int
    expiration_date: str
    expiration_type: str
    option_type: OptionType
    root_symbol: str
    greeks: Optional[Greeks]


class Options(BaseModel):
    option: List[OptionContract]


class Strikes(BaseModel):
    strike: List[float]


class Expirations(BaseModel):
    date: List[str]


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
    start: str
    end: str


class Open(BaseModel):
    start: str
    end: str


class Postmarket(BaseModel):
    start: str
    end: str


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
