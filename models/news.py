from dataclasses import dataclass
from typing import List, Optional


@dataclass
class News:
    url: str
    date: str
    website: str
    source: str
    title: str
    text: Optional[str] = None
    currencies: Optional[List[str]] = None
    hashtags: Optional[List[str]] = None
    is_short: Optional[bool] = None
