from models.news import News
from typing import List
import requests

from config import CRYPTOPANIC_AUTH_TOKEN


class NewsFetcher:
    def get_news_from_twitter(self):
        # Здесь должен быть код для получения новостей из Twitter
        pass

    @staticmethod
    def get_news_from_cryptopanic() -> List[News]:
        base_url = 'https://cryptopanic.com/api/v1/posts/'
        params = {'auth_token': CRYPTOPANIC_AUTH_TOKEN}

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        results = response.json()['results']

        return [
            News(
                url=result['url'],
                date=result['published_at'],
                website=result['domain'],
                source=result['source']['title'],
                title=result['title'],
                currencies=[res['code'] for res in currencies] if (currencies := result.get('currencies')) else []
            ) for result in results
        ]
