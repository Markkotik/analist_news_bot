from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict

from models.news import News


class CandleDuration(Enum):
    ONE_MIN = '1m'
    FIVE_MIN = '5m'
    TEN_MIN = '10m'
    THIRTY_MIN = '30m'
    ONE_HOUR = '1h'

@dataclass
class CandleData:
    prev_close_2: float
    prev_close_1: float
    current_close: float
    next_close_1: float
    next_close_2: float
    next_close_3: float

@dataclass
class BacktestNews(News):
    candle_data: Dict[CandleDuration, CandleData] = field(default_factory=dict)
