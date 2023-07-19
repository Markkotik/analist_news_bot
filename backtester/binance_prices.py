from datetime import datetime, timedelta
from time import sleep
from json import dumps
from requests import get, exceptions

from models.backtestnews import BacktestNews, CandleDuration, CandleData
from models.news import News


def request_binance_data(symbol: str, interval: str, start_dt: int, end_dt: int, retries: int=10) -> list:
    for _ in range(retries):
        try:
            response = get(
                'https://api.binance.com/api/v3/klines',
                params={
                    'symbol': symbol,
                    'interval': interval,
                    'startTime': start_dt,
                    'endTime': end_dt,
                    'limit': 1000,
                },
            )
            response_data = response.json()
            if isinstance(response_data, dict):
                raise ValueError(dumps(response_data))
            return response_data
        except (exceptions.ConnectionError, exceptions.Timeout):
            sleep(1)
    raise ConnectionError("Unable to fetch Binance data after {} retries".format(retries))

def parse_binance_data(binance_data: list) -> dict:
    data = {'open_time': [], 'o': [], 'h': [], 'l': [], 'c': []}
    for row in binance_data:
        data['open_time'].append(row[0])
        data['o'].append(float(row[1]))
        data['h'].append(float(row[2]))
        data['l'].append(float(row[3]))
        data['c'].append(float(row[4]))
    return data

def get_binance_klines(symbol: str, interval: str, start_dt: datetime, end_dt: datetime) -> dict:
    start_dt_ms = int(start_dt.timestamp() * 1000)
    end_dt_ms = int(end_dt.timestamp() * 1000)

    all_data = {'open_time': [], 'o': [], 'h': [], 'l': [], 'c': []}
    while True:
        binance_data = request_binance_data(symbol, interval, start_dt_ms, end_dt_ms)
        parsed_data = parse_binance_data(binance_data)
        for key in all_data:
            all_data[key].extend(parsed_data[key])
        if len(binance_data) < 1000:
            break
        else:
            start_dt_ms = all_data['open_time'][-1] + 1
            sleep(1)
    return all_data

def get_start_end_time(duration: str, current_time: datetime) -> tuple:
    duration_minutes = int(duration[:-1]) # Remove 'm' or 'h' and convert to integer
    if duration.endswith('h'):
        duration_minutes *= 60  # Convert hours to minutes

    # Duration in terms of timedelta
    duration_delta = timedelta(minutes=duration_minutes)

    # Two candles before the current one
    start_time = current_time - 2 * duration_delta

    # Three candles after the current one
    end_time = current_time + 3 * duration_delta

    return start_time, end_time


def fill_candle_data(news: BacktestNews, symbol: str, get_binance_klines, get_start_end_time) -> BacktestNews:
    # Проходим по всем значениям CandleDuration
    for duration in CandleDuration:
        # Получаем начальное и конечное время для текущей продолжительности
        start_time, end_time = get_start_end_time(duration.value, datetime.strptime(news.date, "%Y-%m-%d"))

        # Получаем свечные данные от Binance API
        klines = get_binance_klines(symbol, duration.value, start_time, end_time)

        # Считаем нужные показатели и сохраняем в объект CandleData
        candle_data = CandleData(
            prev_close_1=klines['c'][-2],  # теперь это первый элемент в списке
            prev_close_2=klines['c'][-3],
            current_close=klines['c'][-1],  # теперь это второй элемент в списке
            next_close_1=klines['c'][0],  # предполагаем, что 0 это следующий период
            next_close_2=klines['c'][1],  # предполагаем, что 1 это период после следующего
            next_close_3=klines['c'][2],  # предполагаем, что 2 это период после следующего периода
        )

        # Добавляем полученные данные в BacktestNews
        news.candle_data[duration] = candle_data

    return news


def create_backtest_news(news: News, symbol: str, get_binance_klines, get_start_end_time) -> BacktestNews:
    # Создаем новый экземпляр BacktestNews, используя атрибуты экземпляра News
    backtest_news = BacktestNews(
        url=news.url,
        date=news.date,
        website=news.website,
        source=news.source,
        title=news.title,
        text=news.text,
        currencies=news.currencies,
        hashtags=news.hashtags,
        interpretation=news.interpretation,
        reason=news.reason,
        trade_executed=news.trade_executed,
    )

    # Заполняем свечные данные для новости
    backtest_news = fill_candle_data(backtest_news, symbol, get_binance_klines, get_start_end_time)

    return backtest_news
