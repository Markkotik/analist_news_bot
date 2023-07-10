from dataclasses import dataclass

from database_handler.database_handler import DatabaseHandler
from news_analyser.news_analyser import NewsAnalyser
from news_fetcher.news_fetcher import NewsFetcher


@dataclass
class BotController:
    news_fetcher: NewsFetcher
    news_analyser: NewsAnalyser
    db_handler: DatabaseHandler(db_name='backtest')

    def fetch_and_analyse(self):
        news = self.news_fetcher.get_news_from_cryptopanic(page=10)
        analysis = self.news_analyser.analyse_news(news)
        self.db_handler.save_news_list(analysis)

    def run(self):
        while True:
            self.fetch_and_analyse()

