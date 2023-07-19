import json
import sqlite3
from typing import List, Optional

from models.news import News, Interpretation

# moved SQL related stuff to its own module.
from database_handler.sql import  NEWS_TABLE_SQL, INSERT_NEWS_SQL, SELECT_ALL_NEWS_SQL


class DatabaseHandler:
    def __init__(self, db_name: str = ':memory:'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        self.cursor.execute(NEWS_TABLE_SQL)

    def save_news_list(self, news_list: List[News]):
        for news in news_list:
            self._insert_news(news)

    def save_news(self, news: News):
        self._insert_news(news)

    def _insert_news(self, news: News):
        self.cursor.execute(INSERT_NEWS_SQL, self._to_db_record(news))
        self.conn.commit()

    def get_all_news(self):
        self.cursor.execute(SELECT_ALL_NEWS_SQL)
        return [self._to_news(record) for record in self.cursor.fetchall()]

    def close(self):
        self.conn.close()

    @staticmethod
    def _to_db_record(news: News) -> tuple:
        return (
            news.url,
            news.date,
            news.website,
            news.source,
            news.title,
            news.asset,
            news.text,
            DatabaseHandler._json_dumps(news.currencies),
            DatabaseHandler._json_dumps(news.hashtags),
            news.interpretation.value if news.interpretation is not None else None,
            news.reason,
            news.trade_executed
        )

    @staticmethod
    def _to_news(record: tuple) -> News:
        return News(
            url=record[0],
            date=record[1],
            website=record[2],
            source=record[3],
            title=record[4],
            asset=record[5],
            text=record[6],
            currencies=DatabaseHandler._json_loads(record[7]),
            hashtags=DatabaseHandler._json_loads(record[8]),
            interpretation=Interpretation(record[9]) if record[9] is not None else None,
            reason=record[10],
            trade_executed=record[11],
        )

    # Helper methods for cleaner code: handle json serialization/deserialization.
    @staticmethod
    def _json_dumps(data: Optional[object]) -> Optional[str]:
        return json.dumps(data) if data is not None else None

    @staticmethod
    def _json_loads(data: Optional[str]) -> Optional[object]:
        return json.loads(data) if data is not None else None
