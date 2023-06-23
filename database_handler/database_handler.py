import sqlite3
from models.news import News
# from models.signal import Signal
# from models.trade import Trade


class DatabaseHandler:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS News (
                url TEXT,
                date TEXT,
                website TEXT,
                source TEXT,
                title TEXT,
                text TEXT,
                currencies TEXT,
                hashtags TEXT,
                is_short INTEGER
            )
        """)
        # self.cursor.execute("""
        #     CREATE TABLE IF NOT EXISTS Signals (
        #         signal_id INTEGER PRIMARY KEY,
        #         signal_type TEXT,
        #         signal_time TEXT,
        #         related_news_url TEXT
        #     )
        # """)
        # self.cursor.execute("""
        #     CREATE TABLE IF NOT EXISTS Trades (
        #         trade_id INTEGER PRIMARY KEY,
        #         trade_type TEXT,
        #         trade_time TEXT,
        #         trade_volume REAL,
        #         related_signal_id INTEGER,
        #         FOREIGN KEY(related_signal_id) REFERENCES Signals(signal_id)
        #     )
        # """)
        self.connection.commit()

    def insert_news(self, news: News):
        self.cursor.execute("""
            INSERT INTO News (url, date, website, source, title, text, currencies, hashtags, is_short) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (news.url, news.date, news.website, news.source, news.title, news.text, str(news.currencies), str(news.hashtags), news.is_short))
        self.connection.commit()

    # def insert_signal(self, signal: Signal):
    #     self.cursor.execute("""
    #         INSERT INTO Signals (signal_id, signal_type, signal_time, related_news_url)
    #         VALUES (?, ?, ?, ?)
    #     """, (signal.signal_id, signal.signal_type, signal.signal_time, signal.related_news_url))
    #     self.connection.commit()
    #
    # def insert_trade(self, trade: Trade):
    #     self.cursor.execute("""
    #         INSERT INTO Trades (trade_id, trade_type, trade_time, trade_volume, related_signal_id)
    #         VALUES (?, ?, ?, ?, ?)
    #     """, (trade.trade_id, trade.trade_type, trade.trade_time, trade.trade_volume, trade.related_signal_id))
    #     self.connection.commit()

    def close_connection(self):
        self.connection.close()
