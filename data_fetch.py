import requests
import pandas as pd
from datetime import datetime


API_KEY = '26d4fc03c2bf406398d5e4a16e10442c'
def fetch_finance_news():
    url = f'https://newsapi.org/v2/everything?q=finance&language=en&sortBy=publishedAt&apiKey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    articles = data.get('articles', [])
    df = pd.DataFrame([{
        'title': a['title'],
        'description': a['description'],
        'content': a['content'],
        'url': a['url'],
        'publishedAt': a['publishedAt'],
        'source': a['source']['name']
    } for a in articles])
    df.to_csv('finance_news_raw.csv', index=False)
    print('Finance news fetched and saved.')


if __name__ == '__main__':
    fetch_finance_news()