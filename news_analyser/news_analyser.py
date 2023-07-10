import openai
from typing import List, Tuple, Optional
from config import OPENAI_API_KEY, PROMT_ANALYSIS_TITLES
from models.news import News, Interpretation


class NewsAnalyser:
    def __init__(self):
        openai.api_key = OPENAI_API_KEY
        self.prompt = PROMT_ANALYSIS_TITLES

    def analyse_news(self, news_list: List[News]) -> List[News]:
        for news in news_list:
            interpretation, reason = self.get_interpretation_and_reason(news.title)
            news.interpretation = Interpretation(interpretation)
            news.reason = reason

        return news_list

    def get_interpretation_and_reason(self, title: str) -> Tuple[Optional[str], Optional[str]]:
        input_text = self.prompt + '\n' + title

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=input_text,
            max_tokens=60,
            temperature=0.1,
        )

        if response.choices:
            interpretation, reason = response.choices[0].text.strip().split(':', 1)
            interpretation = ''.join(char for char in interpretation if char.isalpha())

            return interpretation, reason.strip()

        return None, None
