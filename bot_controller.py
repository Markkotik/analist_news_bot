from dataclasses import dataclass

from database_handler.database_handler import DatabaseHandler
from news_fetcher.news_fetcher import NewsFetcher


@dataclass
class BotController:
    news_fetcher: NewsFetcher
    news_analyser: NewsAnalyser
    binance_trader: BinanceTrader
    db_handler: DatabaseHandler

    def fetch_and_analyse(self):
        news = self.news_fetcher.get_latest_news()
        analysis = self.news_analyser.analyse_news(news)
        return analysis

    def decide_and_trade(self, analysis):
        if analysis < 0:
            trade = self.binance_trader.open_short_trade("BTC")
            self.db_handler.save_trade(trade)

    def run(self):
        while True:
            analysis = self.fetch_and_analyse()
            self.decide_and_trade(analysis)
