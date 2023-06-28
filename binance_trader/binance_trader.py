from typing import List
from binance.client import Client
from models.news import News, Interpretation


class BinanceTrader:
    def __init__(self, api_key: str, api_secret: str):
        self.client = Client(api_key, api_secret)

    def get_account_info(self):
        return self.client.get_account()

    def get_market_data(self, symbol: str):
        return self.client.get_ticker(symbol=symbol)

    def place_buy_order(self, symbol: str, quantity: float):
        order = self.client.order_market_buy(
            symbol=symbol,
            quantity=quantity)
        return order

    def place_sell_order(self, symbol: str, quantity: float):
        order = self.client.order_market_sell(
            symbol=symbol,
            quantity=quantity)
        return order

    def analyze_and_trade(self, news_list: List[News]):
        for news in news_list:
            if news.interpretation == Interpretation.BUY:
                self.place_buy_order(news.currency, 1)  # replace with your own logic
            elif news.interpretation == Interpretation.SELL:
                self.place_sell_order(news.currency, 1)  # replace with your own logic
