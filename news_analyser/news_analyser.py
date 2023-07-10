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
            news.interpretation = Interpretation(interpretation.upper())
            news.reason = reason

        return news_list

    def get_interpretation_and_reason(self, title: str) -> Tuple[Optional[str], Optional[str]]:
        input_text = self.prompt + '\n' + title
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0301",
                messages=[
                    {"role": "system", "content": input_text},
                ],
                max_tokens=60,
                temperature=0.1,
            )
            if response['choices']:
                interpretation, reason = response['choices'][0]['message']['content'].strip().split(':', 1)
                interpretation = ''.join(char for char in interpretation if char.isalpha())
                return interpretation, reason.strip()
            else:
                return None, None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None, None
