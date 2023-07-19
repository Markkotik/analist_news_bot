from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class Interpretation(Enum):
    BUY = 'BUY'
    SELL = 'SELL'
    HOLD = 'HOLD'


@dataclass
class News:
    url: str
    date: str
    website: str
    source: str
    title: str
    asset: Optional[str] = None
    text: Optional[str] = None
    currencies: Optional[List[str]] = None
    hashtags: Optional[List[str]] = None
    interpretation: Optional[Interpretation] = None
    reason: Optional[str] = None
    trade_executed: Optional[bool] = None
