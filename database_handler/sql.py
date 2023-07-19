NEWS_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS news (
        url TEXT,
        date TEXT,
        website TEXT,
        source TEXT,
        title TEXT,
        asset TEXT,
        text TEXT,
        currencies TEXT,
        hashtags TEXT,
        interpretation TEXT,
        reason TEXT,
        trade_executed BOOLEAN
    )
"""

INSERT_NEWS_SQL = """
    INSERT INTO news VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

SELECT_ALL_NEWS_SQL = """
    SELECT * FROM news
"""
