from datetime import datetime, timedelta
from time import sleep
from json import dumps
from requests import get, exceptions

from models.backtestnews import BacktestNews, CandleDuration, CandleData
from models.news import News


class BinanceAPI:
    BASE_URL = 'https://api.binance.com/api/v3/klines'
    MAX_RETRIES = 10

    def __init__(self, symbol: str, interval: str):
        self.symbol = symbol
        self.interval = interval

    def fetch_data(self, start_dt: int, end_dt: int) -> list:
        for _ in range(self.MAX_RETRIES):
            try:
                response = self._send_request(start_dt, end_dt)
                return self._validate_and_extract_response(response)
            except (exceptions.ConnectionError, exceptions.Timeout):
                sleep(1)
        raise ConnectionError(f"Unable to fetch Binance data after {self.MAX_RETRIES} retries")

    def _send_request(self, start_dt, end_dt):
        return get(
            self.BASE_URL,
            params={
                'symbol': self.symbol,
                'interval': self.interval,
                'startTime': start_dt,
                'endTime': end_dt,
                'limit': 1000,
            },
        )

    @staticmethod
    def _validate_and_extract_response(response):
        response_data = response.json()
        if isinstance(response_data, dict):
            raise ValueError(dumps(response_data))
        return response_data


class BinanceDataParser:
    def __init__(self, binance_data: list):
        self.binance_data = binance_data

    def parse(self) -> dict:
        data = {'open_time': [], 'o': [], 'h': [], 'l': [], 'c': []}
        for row in self.binance_data:
            data['open_time'].append(row[0])
            data['o'].append(float(row[1]))
            data['h'].append(float(row[2]))
            data['l'].append(float(row[3]))
            data['c'].append(float(row[4]))
        return data


def get_binance_klines(asset: str, interval: str, start_dt: datetime, end_dt: datetime) -> dict:
    start_dt_ms = int(start_dt.timestamp() * 1000)
    end_dt_ms = int(end_dt.timestamp() * 1000)

    all_data = {'open_time': [], 'o': [], 'h': [], 'l': [], 'c': []}
    binance_api = BinanceAPI(asset, interval)

    while True:
        binance_data = binance_api.fetch_data(start_dt_ms, end_dt_ms)
        parsed_data = BinanceDataParser(binance_data).parse()

        for key in all_data:
            all_data[key].extend(parsed_data[key])

        if len(binance_data) < 1000:
            break

        start_dt_ms = all_data['open_time'][-1] + 1
        sleep(1)

    return all_data


def get_start_end_time(duration: str, current_time: datetime) -> tuple:
    duration_minutes = int(duration[:-1])  # Remove 'm' or 'h' and convert to integer
    if duration.endswith('h'):
        duration_minutes *= 60  # Convert hours to minutes

    duration_delta = timedelta(minutes=duration_minutes)

    start_time = current_time - 2 * duration_delta
    end_time = current_time + 3 * duration_delta

    return start_time, end_time


def fill_candle_data(news: BacktestNews, asset: str) -> BacktestNews:
    for duration in CandleDuration:
        start_time, end_time = get_start_end_time(duration.value, datetime.strptime(news.date, "%Y-%m-%d"))
        klines = get_binance_klines(asset, duration.value, start_time, end_time)

        candle_data = CandleData(
            prev_close_2=klines['c'][-0],
            prev_close_1=klines['c'][-1],
            current_close=klines['c'][2],
            next_close_1=klines['c'][3],
            next_close_2=klines['c'][4],
            next_close_3=klines['c'][5],
        )

        news.candle_data[duration] = candle_data

    return news


def create_backtest_news(news: News) -> BacktestNews:
    backtest_news = BacktestNews.from_news(news)
    backtest_news = fill_candle_data(backtest_news, news.asset)

    return backtest_news
