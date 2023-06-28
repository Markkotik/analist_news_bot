import json
import sqlite3
from typing import List

from models.news import News, Interpretation


class DatabaseHandler:
    def __init__(self, db_name: str = ':memory:'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS news (
                url TEXT,
                date TEXT,
                website TEXT,
                source TEXT,
                title TEXT,
                text TEXT,
                currencies TEXT,
                hashtags TEXT,
                interpretation TEXT,
                reason TEXT,
                trade_executed BOOLEAN
            )
        """)

    def save_news(self, news_list: List[News]):
        for news in news_list:
            self.insert_news(news)

    def insert_news(self, news: News):
        self.cursor.execute("""
            INSERT INTO news VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            news.url,
            news.date,
            news.website,
            news.source,
            news.title,
            news.text,
            json.dumps(news.currencies) if news.currencies is not None else None,
            json.dumps(news.hashtags) if news.hashtags is not None else None,
            news.interpretation.value if news.interpretation is not None else None,
            news.reason,
            news.trade_executed
        ))
        self.conn.commit()

    def get_all_news(self):
        self.cursor.execute("""
            SELECT * FROM news
        """)
        rows = self.cursor.fetchall()
        news_list = []
        for row in rows:
            news = News(
                url=row[0],
                date=row[1],
                website=row[2],
                source=row[3],
                title=row[4],
                text=row[5],
                currencies=json.loads(row[6]) if row[6] is not None else None,
                hashtags=json.loads(row[7]) if row[7] is not None else None,
                interpretation=Interpretation(row[8]) if row[8] is not None else None,
                reason=row[9],
                trade_executed=row[10]
            )
            news_list.append(news)
        return news_list

    def close(self):
        self.conn.close()
