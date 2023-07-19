from dataclasses import dataclass, field
from binance.client import Client
from typing import Optional
from config import BINANCE_API_KEY, BINANCE_SECRET_KEY, BINANCE_STABLECOINS


@dataclass
class BinanceChecker:
    stablecoins: list[str] = BINANCE_STABLECOINS
    client: Client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)
    ticker_set: set[str] = field(default_factory=lambda: {ticker['symbol'] for ticker in Client(BINANCE_API_KEY,
                                                                                                BINANCE_SECRET_KEY).get_all_tickers()})

    def is_traded_on_binance(self, coin: str) -> bool:
        coin = coin.upper() + 'USDT'
        return coin in self.ticker_set

    def get_tradable_asset(self, coins: list[str]) -> Optional[str]:
        coins = [coin.upper() for coin in coins]
        if not coins:
            return 'BTCUSDT'

        coins = [coin for coin in coins if coin not in ['BTC'] + self.stablecoins]
        for coin in reversed(coins):
            if self.is_traded_on_binance(coin):
                return coin + 'USDT'
        return None
