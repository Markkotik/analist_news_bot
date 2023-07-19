from dataclasses import dataclass, asdict
from typing import List
import pandas as pd

from database_handler.database_handler import DatabaseHandler
from news_analyser.news_analyser import NewsAnalyser
from news_fetcher.news_fetcher import NewsFetcher
from binance_backtest_data import create_backtest_news
from models.backtestnews import BacktestNews


@dataclass
class BotController:
    news_fetcher: NewsFetcher
    news_analyser: NewsAnalyser
    db_handler: DatabaseHandler = DatabaseHandler(db_name='backtest.db')

    def fetch_and_analyse(self):
        news = self.news_fetcher.get_news_from_cryptopanic(page=10)
        analysis = self.news_analyser.analyse_news(news)
        self.db_handler.save_news_list(analysis)

    def add_backtestnews(self):
        news_list = self.db_handler.get_all_news()
        backtest_news_list = [create_backtest_news(news) for news in news_list]
        self.save_backtestnews_to_csv(backtest_news_list)

    @staticmethod
    def save_backtestnews_to_csv(backtest_news_list: List[BacktestNews]):
        backtest_news_dicts = [asdict(bn) for bn in backtest_news_list]
        for bn_dict in backtest_news_dicts:
            for duration, candle_data in bn_dict['candle_data'].items():
                for key, value in candle_data.items():
                    bn_dict[f"{duration}_{key}"] = value
            del bn_dict['candle_data']

        df = pd.DataFrame(backtest_news_dicts)
        df.to_csv('backtest_news.csv', index=False)

    def run(self):
        while True:
            self.fetch_and_analyse()
