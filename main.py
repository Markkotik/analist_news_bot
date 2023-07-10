from binance_trader.binance_trader import BinanceTrader
from database_handler.database_handler import DatabaseHandler
from news_analyser.news_analyser import NewsAnalyser
from news_fetcher.news_fetcher import NewsFetcher
from bot_controller import BotController


def main():
    news_fetcher = NewsFetcher()
    news_analyser = NewsAnalyser()
    binance_trader = BinanceTrader()
    db_handler = DatabaseHandler()

    bot_controller = BotController(
        news_fetcher=news_fetcher,
        news_analyser=news_analyser,
        binance_trader=binance_trader,
        db_handler=db_handler,
    )

    bot_controller.run()


if __name__ == "__main__":
    main()
